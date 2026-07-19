const WORD_CAP = 20;

const state = {
  topic: null,
  scenes: [],
  manifest: {},
  index: 0,
  dirty: false,
};

const $ = (sel) => document.querySelector(sel);
const filmstripEl = $("#filmstrip");
const cardRootEl = $("#card-root");
const topicSelect = $("#topic-select");
const saveBtn = $("#save-btn");
const saveStatus = $("#save-status");

async function fetchJSON(url, opts) {
  const res = await fetch(url, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `request failed: ${url}`);
  return data;
}

async function init() {
  const topics = await fetchJSON("/api/topics");
  topicSelect.innerHTML = topics.map((t) => `<option value="${t}">${t}</option>`).join("");
  topicSelect.addEventListener("change", () => loadTopic(topicSelect.value));
  saveBtn.addEventListener("click", save);
  window.addEventListener("beforeunload", (e) => {
    if (state.dirty) { e.preventDefault(); e.returnValue = ""; }
  });
  state.manifest = await fetchJSON("/api/manifest");
  if (topics.length) {
    topicSelect.value = topics[0];
    await loadTopic(topics[0]);
  }
}

async function loadTopic(topic) {
  const data = await fetchJSON(`/api/topics/${encodeURIComponent(topic)}`);
  state.topic = data.topic || topic;
  state.scenes = data.scenes || [];
  state.index = 0;
  state.dirty = false;
  setSaveStatus("");
  render();
}

function setSaveStatus(text) {
  saveStatus.textContent = text;
}

function markDirty() {
  state.dirty = true;
  setSaveStatus("unsaved changes");
}

function validateScene(scene) {
  const warnings = [];
  if (!scene.visual_action || !scene.visual_action.trim()) {
    warnings.push("visual_action is empty");
  }
  if (!scene.sprite_sequence || scene.sprite_sequence.length < 2) {
    warnings.push("sprite_sequence needs at least 2 entries");
  }
  for (const field of ["incoming", "outgoing"]) {
    const value = scene[field] || "";
    if (!value.trim()) {
      warnings.push(`${field} is empty`);
    } else {
      const wordCount = value.trim().split(/\s+/).length;
      if (wordCount > WORD_CAP) {
        warnings.push(`${field} exceeds ${WORD_CAP}-word cap (${wordCount} words, redundancy risk)`);
      }
    }
  }
  const unknownSprites = (scene.sprite_sequence || []).filter((id) => !state.manifest[id]);
  if (unknownSprites.length) {
    warnings.push(`unknown sprite id(s): ${unknownSprites.join(", ")}`);
  }
  return warnings;
}

function spriteUrl(spriteId) {
  const entry = state.manifest[spriteId];
  if (!entry) return "";
  return `/sprites/${entry.file.replace(/^sprites\//, "")}`;
}

function render() {
  renderFilmstrip();
  renderCard();
}

function renderFilmstrip() {
  if (!state.scenes.length) {
    filmstripEl.innerHTML = "";
    return;
  }
  filmstripEl.innerHTML = state.scenes.map((scene, i) => {
    const thumbSprite = scene.sprite_sequence && scene.sprite_sequence[0];
    const img = thumbSprite ? `<img src="${spriteUrl(thumbSprite)}" alt="">` : "";
    return `
      <div class="thumb ${i === state.index ? "active" : ""}" data-index="${i}">
        ${img}
        <div class="thumb-label"><span class="status-dot ${scene.status}"></span>${scene.page_id}</div>
      </div>
    `;
  }).join("");
  filmstripEl.querySelectorAll(".thumb").forEach((el) => {
    el.addEventListener("click", () => selectIndex(Number(el.dataset.index)));
  });
}

function selectIndex(i) {
  if (i < 0 || i >= state.scenes.length) return;
  state.index = i;
  render();
}

function renderCard() {
  if (!state.scenes.length) {
    cardRootEl.innerHTML = `<p class="empty-state">No scenes in this topic yet.</p>`;
    return;
  }
  const scene = state.scenes[state.index];
  const warnings = validateScene(scene);

  const spriteCells = (scene.sprite_sequence || []).map((id) => `
    <div class="sprite-cell">
      <img src="${spriteUrl(id)}" alt="${id}">
      <div class="sprite-id">${id}</div>
    </div>
  `).join("") || `<p class="empty-state">No sprites in sequence.</p>`;

  cardRootEl.innerHTML = `
    <div class="card">
      <div class="card-header">
        <h2>${scene.page_id}</h2>
        <span class="badge ${scene.status}">${scene.status}</span>
      </div>

      <div class="nav-row">
        <div class="group">
          <button id="prev-btn" ${state.index === 0 ? "disabled" : ""}>&larr; Prev</button>
          <button id="next-btn" ${state.index === state.scenes.length - 1 ? "disabled" : ""}>Next &rarr;</button>
          <span class="empty-state">${state.index + 1} / ${state.scenes.length}</span>
        </div>
        <div class="group">
          <button id="move-up-btn" ${state.index === 0 ? "disabled" : ""}>Move Up</button>
          <button id="move-down-btn" ${state.index === state.scenes.length - 1 ? "disabled" : ""}>Move Down</button>
          <button id="clone-btn">Clone</button>
          <button id="toggle-ready-btn" class="primary">${scene.status === "ready" ? "Mark Draft" : "Mark Ready"}</button>
        </div>
      </div>

      <div class="sprite-row">${spriteCells}</div>

      <div class="field">
        <label>visual_action</label>
        <textarea id="visual-action-field">${escapeHtml(scene.visual_action || "")}</textarea>
      </div>

      <div class="field-row">
        <div class="field">
          <label>incoming</label>
          <textarea id="incoming-field">${escapeHtml(scene.incoming || "")}</textarea>
        </div>
        <div class="field">
          <label>outgoing</label>
          <textarea id="outgoing-field">${escapeHtml(scene.outgoing || "")}</textarea>
        </div>
      </div>

      <div class="field-row">
        <div class="field">
          <label>domain</label>
          <input id="domain-field" value="${escapeHtml(scene.domain || "")}">
        </div>
        <div class="field">
          <label>exam_ref</label>
          <input id="exam-ref-field" value="${escapeHtml(scene.exam_ref || "")}">
        </div>
      </div>

      <div class="field">
        <label>notes</label>
        <input id="notes-field" value="${escapeHtml(scene.notes || "")}">
      </div>

      <div class="warnings ${warnings.length ? "" : "hidden"}">
        <strong>${warnings.length} validation warning(s)</strong>
        <ul>${warnings.map((w) => `<li>${w}</li>`).join("")}</ul>
      </div>
    </div>
  `;

  bindCardEvents(scene);
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function bindCardEvents(scene) {
  $("#prev-btn")?.addEventListener("click", () => selectIndex(state.index - 1));
  $("#next-btn")?.addEventListener("click", () => selectIndex(state.index + 1));
  $("#move-up-btn")?.addEventListener("click", () => moveScene(-1));
  $("#move-down-btn")?.addEventListener("click", () => moveScene(1));
  $("#clone-btn")?.addEventListener("click", cloneScene);
  $("#toggle-ready-btn")?.addEventListener("click", () => {
    scene.status = scene.status === "ready" ? "draft" : "ready";
    markDirty();
    render();
  });

  const bindField = (elId, sceneField) => {
    $(elId)?.addEventListener("input", (e) => {
      scene[sceneField] = e.target.value;
      markDirty();
    });
    $(elId)?.addEventListener("blur", () => render());
  };
  bindField("#visual-action-field", "visual_action");
  bindField("#incoming-field", "incoming");
  bindField("#outgoing-field", "outgoing");
  bindField("#domain-field", "domain");
  bindField("#exam-ref-field", "exam_ref");
  bindField("#notes-field", "notes");
}

function moveScene(delta) {
  const newIndex = state.index + delta;
  if (newIndex < 0 || newIndex >= state.scenes.length) return;
  const [scene] = state.scenes.splice(state.index, 1);
  state.scenes.splice(newIndex, 0, scene);
  state.index = newIndex;
  markDirty();
  render();
}

function nextPageId(basePageId, existingIds) {
  const match = basePageId.match(/^(.*?)(\d+)$/);
  if (match) {
    const [, prefix, numStr] = match;
    let num = parseInt(numStr, 10);
    const width = numStr.length;
    let candidate;
    do {
      num += 1;
      candidate = `${prefix}${String(num).padStart(width, "0")}`;
    } while (existingIds.has(candidate));
    return candidate;
  }
  let suffix = 2;
  let candidate = `${basePageId}-copy`;
  while (existingIds.has(candidate)) {
    candidate = `${basePageId}-copy${suffix}`;
    suffix += 1;
  }
  return candidate;
}

function cloneScene() {
  const original = state.scenes[state.index];
  const existingIds = new Set(state.scenes.map((s) => s.page_id));
  const clone = JSON.parse(JSON.stringify(original));
  clone.page_id = nextPageId(original.page_id, existingIds);
  clone.status = "draft";
  state.scenes.splice(state.index + 1, 0, clone);
  state.index += 1;
  markDirty();
  render();
}

async function save() {
  setSaveStatus("saving...");
  try {
    await fetchJSON(`/api/topics/${encodeURIComponent(state.topic)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: state.topic, scenes: state.scenes }),
    });
    state.dirty = false;
    setSaveStatus("saved");
  } catch (err) {
    setSaveStatus(`save failed: ${err.message}`);
  }
}

init();
