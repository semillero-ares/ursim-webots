#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
#  URSim + Webots installer for Ubuntu 24.04
#  Usage: curl -fsSL https://semillero-ares.github.io/ursim-webots/install.sh | bash
# ─────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

WORKDIR="$HOME/ursim-webots"
REPO="https://github.com/semillero-ares/ursim-webots.git"

log()     { echo -e "${CYAN}${BOLD}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}${BOLD}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}${BOLD}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}${BOLD}[ERROR]${RESET} $*"; exit 1; }
step()    { echo -e "\n${BOLD}━━━  $*  ━━━${RESET}"; }

require_ubuntu() {
  if [[ ! -f /etc/os-release ]]; then
    error "Cannot detect OS. This script requires Ubuntu 24.04."
  fi
  # shellcheck source=/dev/null
  source /etc/os-release
  if [[ "$ID" != "ubuntu" ]]; then
    error "This script is designed for Ubuntu. Detected: $ID"
  fi
  if [[ "$VERSION_ID" != "24.04" ]]; then
    warn "This script was tested on Ubuntu 24.04. Detected: $VERSION_ID. Proceeding anyway..."
  fi
}

require_sudo() {
  if ! sudo -v 2>/dev/null; then
    error "This script requires sudo privileges."
  fi
  # Keep sudo alive throughout the script
  while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &
}

# ── 1. Git ────────────────────────────────────
install_git() {
  step "Step 1 / 4 — Git"
  if command -v git &>/dev/null; then
    success "Git already installed: $(git --version)"
    return
  fi
  log "Installing Git..."
  sudo apt-get update -qq
  sudo apt-get install -y git
  success "Git installed: $(git --version)"
}

# ── 2. Python ────────────────────────────────
install_python() {
  step "Step 2 / 4 — Python"
  if command -v python3 &>/dev/null; then
    success "Python already installed: $(python3 --version)"
  else
    log "Installing Python 3..."
    sudo apt-get install -y python3
    success "Python installed: $(python3 --version)"
  fi

  log "Ensuring pip is available..."
  sudo apt-get install -y python3-pip
  success "pip ready: $(python3 -m pip --version)"
}

# ── 3. Webots ────────────────────────────────
install_webots() {
  step "Step 3 / 4 — Webots"
  if command -v webots &>/dev/null; then
    success "Webots already installed."
    return
  fi
  log "Adding Cyberbotics apt repository..."
  sudo apt-get install -y wget gnupg
  wget -qO- https://cyberbotics.com/Cyberbotics.asc \
    | sudo gpg --dearmor -o /etc/apt/keyrings/cyberbotics.gpg
  echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/cyberbotics.gpg] \
https://cyberbotics.com/debian/ binary-amd64/" \
    | sudo tee /etc/apt/sources.list.d/cyberbotics.list > /dev/null
  sudo apt-get update -qq
  log "Installing Webots (this may take a while)..."
  sudo apt-get install -y webots
  success "Webots installed."
}

# ── 4. Docker Engine ─────────────────────────
install_docker() {
  step "Step 4 / 4 — Docker Engine"
  if command -v docker &>/dev/null; then
    success "Docker already installed: $(docker --version)"
  else
    log "Installing Docker Engine..."
    sudo apt-get install -y ca-certificates curl gnupg lsb-release

    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
      | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
      | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -qq
    sudo apt-get install -y \
      docker-ce docker-ce-cli containerd.io \
      docker-buildx-plugin docker-compose-plugin
    success "Docker installed: $(docker --version)"
  fi

  # Add user to docker group
  if ! groups "$USER" | grep -q docker; then
    log "Adding $USER to the docker group..."
    sudo usermod -aG docker "$USER"
    warn "Group change will take effect after you log out and back in."
    warn "For this session, commands below will use 'sudo docker'."
    DOCKER_CMD="sudo docker"
  else
    DOCKER_CMD="docker"
    success "User $USER is already in the docker group."
  fi
}

# ── Project setup ────────────────────────────
setup_project() {
  step "Project — Clone & Configure"

  if [[ -d "$WORKDIR/.git" ]]; then
    success "Repository already cloned at $WORKDIR"
  else
    log "Cloning repository into $WORKDIR ..."
    mkdir -p "$WORKDIR"
    git clone "$REPO" "$WORKDIR"
  fi

  cd "$WORKDIR"

  log "Installing Python requirements..."
  python3 -m pip install --upgrade pip --break-system-packages 2>/dev/null \
    || python3 -m pip install --upgrade pip
  python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null \
    || python3 -m pip install -r requirements.txt

  success "Python packages installed."

  log "Creating Docker virtual network 'dockernet'..."
  if $DOCKER_CMD network ls --format '{{.Name}}' | grep -q '^dockernet$'; then
    warn "Network 'dockernet' already exists — skipping."
  else
    $DOCKER_CMD network create \
      -d bridge \
      --subnet 192.168.0.0/24 \
      --gateway 192.168.0.1 \
      dockernet
    success "Network 'dockernet' created."
  fi

  log "Starting URSim container..."
  cd "$WORKDIR/ursim"
  $DOCKER_CMD compose up -d
  success "URSim container started."
}

# ── Summary ──────────────────────────────────
print_summary() {
  LOCAL_IP=$(ip addr show | awk '/inet / && !/127\.0\.0\.1/{print $2}' | cut -d/ -f1 | head -1)

  echo ""
  echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════╗"
  echo -e "║         Installation complete! 🎉        ║"
  echo -e "╚══════════════════════════════════════════╝${RESET}"
  echo ""
  echo -e "  ${BOLD}URSim browser interface:${RESET}"
  echo -e "    → ${CYAN}http://localhost:6080/vnc.html${RESET}"
  echo ""
  echo -e "  ${BOLD}Your local IP (for RealVNC):${RESET}"
  echo -e "    → ${CYAN}${LOCAL_IP:-<run: ip addr show>}${RESET}"
  echo ""
  echo -e "  ${BOLD}To stop the simulator:${RESET}"
  echo -e "    cd $WORKDIR/ursim && docker compose down"
  echo ""
  if groups "$USER" | grep -q docker; then
    : # already in group, no extra warning
  else
    echo -e "  ${YELLOW}${BOLD}Remember:${RESET} Log out and back in so Docker works without sudo."
    echo ""
  fi
}

# ── Main ─────────────────────────────────────
main() {
  echo ""
  echo -e "${BOLD}  URSim + Webots — Ubuntu 24.04 Installer${RESET}"
  echo -e "  ─────────────────────────────────────────"
  echo ""

  require_ubuntu
  require_sudo
  install_git
  install_python
  install_webots
  install_docker
  setup_project
  print_summary
}

main "$@"