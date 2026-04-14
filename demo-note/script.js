const STORAGE_KEY_STATE = "demo.note.panel.state";
const STORAGE_KEY_NOTES = "demo.note.node.notes";

const nodeGrid = document.getElementById("nodeGrid");
const notePanel = document.getElementById("notePanel");
const noteHeader = document.getElementById("noteHeader");
const noteContent = document.getElementById("noteContent");
const noteLauncher = document.getElementById("noteLauncher");
const selectedNodeLabel = document.getElementById("selectedNodeLabel");
const saveStatus = document.getElementById("saveStatus");
const resizeHandle = document.getElementById("resizeHandle");
const debugLog = document.getElementById("debugLog");

const collapseBtn = document.getElementById("collapseBtn");
const minimizeBtn = document.getElementById("minimizeBtn");
const closeBtn = document.getElementById("closeBtn");

const fieldName = document.getElementById("fieldName");
const fieldKind = document.getElementById("fieldKind");
const fieldIntent = document.getElementById("fieldIntent");
const fieldStatus = document.getElementById("fieldStatus");

let selectedNodeId = null;
let saveTimer = null;
let hasPendingChanges = false;

let panelState = {
  x: 920,
  y: 360,
  width: 320,
  height: 360,
  collapsed: false,
  minimized: false,
  selectedNodeId: null,
};

function addLog(event, detail = "") {
  const li = document.createElement("li");
  const time = new Date().toLocaleTimeString();
  li.textContent = `${time} | ${event}${detail ? ` | ${detail}` : ""}`;
  debugLog.prepend(li);
  while (debugLog.children.length > 60) debugLog.removeChild(debugLog.lastChild);
}

function loadPanelState() {
  const raw = localStorage.getItem(STORAGE_KEY_STATE);
  if (!raw) return;
  try {
    panelState = { ...panelState, ...JSON.parse(raw) };
  } catch {
    addLog("state_parse_error");
  }
}

function savePanelState() {
  localStorage.setItem(STORAGE_KEY_STATE, JSON.stringify(panelState));
}

function getAllNotes() {
  const raw = localStorage.getItem(STORAGE_KEY_NOTES);
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

function saveNoteForCurrentNode() {
  if (!selectedNodeId) return;
  const notes = getAllNotes();
  notes[selectedNodeId] = {
    name: fieldName.value,
    kind: fieldKind.value,
    intent: fieldIntent.value,
    status: fieldStatus.value,
    updatedAt: new Date().toISOString(),
  };
  localStorage.setItem(STORAGE_KEY_NOTES, JSON.stringify(notes));
  hasPendingChanges = false;
  saveStatus.textContent = "已保存";
  addLog("auto_save", selectedNodeId);
}

function scheduleSave() {
  hasPendingChanges = true;
  saveStatus.textContent = "自动保存中...";
  if (saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNoteForCurrentNode, 500);
}

function loadNodeNote(nodeId) {
  const note = getAllNotes()[nodeId] || {
    name: "",
    kind: "component",
    intent: "",
    status: "draft",
  };
  fieldName.value = note.name;
  fieldKind.value = note.kind;
  fieldIntent.value = note.intent;
  fieldStatus.value = note.status;
  hasPendingChanges = false;
  saveStatus.textContent = "已加载";
}

function setPanelRect() {
  notePanel.style.left = `${panelState.x}px`;
  notePanel.style.top = `${panelState.y}px`;
  notePanel.style.width = `${panelState.width}px`;
  notePanel.style.height = `${panelState.height}px`;
}

function clampPanelToCanvas() {
  const inspectorWidth = 320;
  const maxX = window.innerWidth - inspectorWidth - panelState.width - 8;
  const maxY = window.innerHeight - panelState.height - 8;
  panelState.x = Math.max(8, Math.min(panelState.x, Math.max(8, maxX)));
  panelState.y = Math.max(8, Math.min(panelState.y, Math.max(8, maxY)));
}

function refreshPanelVisibility() {
  notePanel.classList.toggle("hidden", panelState.minimized);
  noteLauncher.classList.toggle("hidden", !panelState.minimized);
  notePanel.classList.toggle("collapsed", panelState.collapsed);
  savePanelState();
}

function selectNode(button) {
  const nextId = button.dataset.nodeId;
  if (selectedNodeId && hasPendingChanges) {
    saveStatus.textContent = "未保存更改，切换节点后将自动保存";
    saveNoteForCurrentNode();
  }

  document.querySelectorAll(".node-card").forEach((card) => card.classList.remove("active"));
  button.classList.add("active");

  selectedNodeId = nextId;
  panelState.selectedNodeId = nextId;
  selectedNodeLabel.textContent = `Selected: ${button.dataset.nodeName}`;
  loadNodeNote(nextId);
  addLog("select_node", nextId);
  savePanelState();
}

nodeGrid.addEventListener("click", (event) => {
  const button = event.target.closest(".node-card");
  if (!button) return;
  selectNode(button);
});

[fieldName, fieldKind, fieldIntent, fieldStatus].forEach((field) => {
  field.addEventListener("input", scheduleSave);
  field.addEventListener("change", scheduleSave);
});

collapseBtn.addEventListener("click", () => {
  panelState.collapsed = !panelState.collapsed;
  refreshPanelVisibility();
  addLog("collapse", String(panelState.collapsed));
});

function minimizePanel() {
  panelState.minimized = true;
  refreshPanelVisibility();
  addLog("minimize");
}

minimizeBtn.addEventListener("click", minimizePanel);
closeBtn.addEventListener("click", minimizePanel);

noteLauncher.addEventListener("click", () => {
  panelState.minimized = false;
  refreshPanelVisibility();
  addLog("restore");
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  if (panelState.minimized) return;

  if (!panelState.collapsed) {
    panelState.collapsed = true;
    addLog("collapse", "esc");
  } else {
    panelState.minimized = true;
    addLog("minimize", "esc");
  }

  refreshPanelVisibility();
});

let dragState = null;

noteHeader.addEventListener("mousedown", (event) => {
  if (event.target.closest("button")) return;
  dragState = {
    startX: event.clientX,
    startY: event.clientY,
    originX: panelState.x,
    originY: panelState.y,
  };
  notePanel.classList.add("dragging");
  addLog("panel_drag_start");
});

window.addEventListener("mousemove", (event) => {
  if (!dragState) return;
  panelState.x = dragState.originX + (event.clientX - dragState.startX);
  panelState.y = dragState.originY + (event.clientY - dragState.startY);
  clampPanelToCanvas();
  setPanelRect();
});

window.addEventListener("mouseup", () => {
  if (!dragState) return;
  dragState = null;
  notePanel.classList.remove("dragging");
  savePanelState();
  addLog("panel_drag_end");
});

let resizeState = null;

resizeHandle.addEventListener("mousedown", (event) => {
  event.stopPropagation();
  resizeState = {
    startX: event.clientX,
    startY: event.clientY,
    startW: panelState.width,
    startH: panelState.height,
  };
});

window.addEventListener("mousemove", (event) => {
  if (!resizeState) return;

  panelState.width = Math.max(280, resizeState.startW + event.clientX - resizeState.startX);
  panelState.height = Math.max(210, resizeState.startH + event.clientY - resizeState.startY);
  clampPanelToCanvas();
  setPanelRect();
  addLog("panel_resize", `${panelState.width}x${panelState.height}`);
});

window.addEventListener("mouseup", () => {
  if (!resizeState) return;
  resizeState = null;
  savePanelState();
});

window.addEventListener("resize", () => {
  clampPanelToCanvas();
  setPanelRect();
  savePanelState();
});

(function init() {
  loadPanelState();
  clampPanelToCanvas();
  setPanelRect();
  refreshPanelVisibility();

  if (panelState.selectedNodeId) {
    const btn = document.querySelector(`[data-node-id="${panelState.selectedNodeId}"]`);
    if (btn) selectNode(btn);
  }

  addLog("init", "demo_ready");
})();
