const API_URL = 'http://127.0.0.1:8000/predict';

const ALL_SYMPTOMS = [
  'abdominal_pain','abnormal_menstruation','acidity','acute_liver_failure',
  'altered_sensorium','anxiety','back_pain','belly_pain','blackheads',
  'bladder_discomfort','blister','blood_in_sputum','bloody_stool',
  'blurred_and_distorted_vision','breathlessness','brittle_nails','bruising',
  'burning_micturition','chest_pain','chills','cold_hands_and_feets','coma',
  'congestion','constipation','continuous_feel_of_urine','continuous_sneezing',
  'cough','cramps','dark_urine','dehydration','depression','diarrhoea',
  'dischromic _patches','distention_of_abdomen','dizziness',
  'drying_and_tingling_lips','enlarged_thyroid','excessive_hunger',
  'extra_marital_contacts','family_history','fast_heart_rate','fatigue',
  'fluid_overload','foul_smell_of urine','headache','high_fever',
  'hip_joint_pain','history_of_alcohol_consumption','increased_appetite',
  'indigestion','inflammatory_nails','internal_itching','irregular_sugar_level',
  'irritability','irritation_in_anus','itching','joint_pain','knee_pain',
  'lack_of_concentration','lethargy','loss_of_appetite','loss_of_balance',
  'loss_of_smell','malaise','mild_fever','mood_swings','movement_stiffness',
  'mucoid_sputum','muscle_pain','muscle_wasting','muscle_weakness','nausea',
  'neck_pain','nodal_skin_eruptions','obesity','pain_behind_the_eyes',
  'pain_during_bowel_movements','pain_in_anal_region','painful_walking',
  'palpitations','passage_of_gases','patches_in_throat','phlegm','polyuria',
  'prominent_veins_on_calf','puffy_face_and_eyes','pus_filled_pimples',
  'receiving_blood_transfusion','receiving_unsterile_injections',
  'red_sore_around_nose','red_spots_over_body','redness_of_eyes','restlessness',
  'runny_nose','rusty_sputum','scurring','shivering','silver_like_dusting',
  'sinus_pressure','skin_peeling','skin_rash','slurred_speech',
  'small_dents_in_nails','spinning_movements','spotting_ urination','stiff_neck',
  'stomach_bleeding','stomach_pain','sunken_eyes','sweating','swelled_lymph_nodes',
  'swelling_joints','swelling_of_stomach','swollen_blood_vessels',
  'swollen_extremeties','swollen_legs','throat_irritation',
  'toxic_look_(typhos)','ulcers_on_tongue','unsteadiness','visual_disturbances',
  'vomiting','watering_from_eyes','weakness_in_limbs','weakness_of_one_body_side',
  'weight_gain','weight_loss','yellow_crust_ooze','yellow_urine',
  'yellowing_of_eyes','yellowish_skin'
];

// ── Format label for display ──────────────────────────────────────────────────
function formatLabel(s) {
  return s.replace(/_/g, ' ').replace(/\s+/g, ' ').trim()
          .replace(/\b\w/g, c => c.toUpperCase());
}

// ── State ─────────────────────────────────────────────────────────────────────
let slots = [];          // array of { id, value }
let slotCount = 0;
const MAX_SLOTS = 17;

// ── Init ──────────────────────────────────────────────────────────────────────
function init() {
  addSlot();  // start with 1 slot
}

// ── Get all currently selected symptoms (excluding empty) ─────────────────────
function getUsedSymptoms() {
  return slots.filter(s => s.value).map(s => s.value);
}

// ── Add a new slot ────────────────────────────────────────────────────────────
function addSlot() {
  if (slots.length >= MAX_SLOTS) return;

  const id = ++slotCount;
  slots.push({ id, value: '' });
  renderSlot(id);
  updateAddBtn();
}

// ── Remove a slot ─────────────────────────────────────────────────────────────
function removeSlot(id) {
  slots = slots.filter(s => s.id !== id);
  const el = document.getElementById(`slot-${id}`);
  if (el) {
    el.style.opacity = '0';
    el.style.transform = 'translateX(-10px)';
    el.style.transition = 'all 0.2s';
    setTimeout(() => { el.remove(); renumberSlots(); }, 200);
  }
  updateAddBtn();
}

// ── Renumber visible slot labels ──────────────────────────────────────────────
function renumberSlots() {
  const nums = document.querySelectorAll('.slot-number');
  nums.forEach((el, i) => { el.textContent = String(i + 1).padStart(2, '0'); });
}

// ── Render a slot into DOM ────────────────────────────────────────────────────
function renderSlot(id) {
  const container = document.getElementById('symptomSlots');
  const index = slots.findIndex(s => s.id === id);

  const div = document.createElement('div');
  div.className = 'slot';
  div.id = `slot-${id}`;
  div.innerHTML = `
    <span class="slot-number">${String(index + 1).padStart(2, '0')}</span>
    <div class="slot-input-wrap" id="wrap-${id}">
      <input
        class="slot-search"
        id="input-${id}"
        type="text"
        placeholder="Search symptom…"
        autocomplete="off"
        oninput="onSearch(${id})"
        onfocus="openDropdown(${id})"
        onkeydown="onKeydown(event, ${id})"
      />
      <svg class="slot-chevron" width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M3 5l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <div class="slot-dropdown" id="dropdown-${id}"></div>
    </div>
    <button class="slot-remove" onclick="removeSlot(${id})" title="Remove">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M3 3l8 8M11 3l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </button>
  `;
  container.appendChild(div);

  // Open dropdown right away on first slot
  if (slots.length === 1) {
    setTimeout(() => openDropdown(id), 100);
  }
}

// ── Open dropdown ─────────────────────────────────────────────────────────────
function openDropdown(id) {
  closeAllDropdowns(id);
  const wrap = document.getElementById(`wrap-${id}`);
  if (wrap) {
    wrap.classList.add('open');
    populateDropdown(id, document.getElementById(`input-${id}`).value);
  }
}

// ── Close all dropdowns except current ───────────────────────────────────────
function closeAllDropdowns(exceptId) {
  document.querySelectorAll('.slot-input-wrap.open').forEach(w => {
    if (w.id !== `wrap-${exceptId}`) w.classList.remove('open');
  });
}

// ── Close all dropdowns ───────────────────────────────────────────────────────
function closeAll() {
  document.querySelectorAll('.slot-input-wrap.open').forEach(w => w.classList.remove('open'));
}

// ── Populate dropdown with filtered options ───────────────────────────────────
function populateDropdown(id, query = '') {
  const dropdown = document.getElementById(`dropdown-${id}`);
  if (!dropdown) return;

  const used = getUsedSymptoms();
  const slotVal = slots.find(s => s.id === id)?.value || '';
  const q = query.toLowerCase().trim();

  let filtered = ALL_SYMPTOMS.filter(sym => {
    const label = formatLabel(sym).toLowerCase();
    return q === '' || label.includes(q) || sym.includes(q);
  });

  dropdown.innerHTML = '';

  if (filtered.length === 0) {
    dropdown.innerHTML = `<div class="dropdown-empty">No symptoms found</div>`;
    return;
  }

  filtered.forEach(sym => {
    const isUsed = used.includes(sym) && sym !== slotVal;
    const label = formatLabel(sym);
    const div = document.createElement('div');
    div.className = 'dropdown-option' + (isUsed ? ' disabled' : '');
    div.textContent = label;
    div.dataset.value = sym;
    if (!isUsed) {
      div.onclick = () => selectSymptom(id, sym);
    }
    dropdown.appendChild(div);
  });
}

// ── On search input ───────────────────────────────────────────────────────────
function onSearch(id) {
  const input = document.getElementById(`input-${id}`);
  const q = input.value;
  const wrap = document.getElementById(`wrap-${id}`);

  // Clear selection if user types
  const slot = slots.find(s => s.id === id);
  if (slot && slot.value) {
    slot.value = '';
    input.classList.remove('has-value');
  }

  wrap.classList.add('open');
  populateDropdown(id, q);
}

// ── Select a symptom ──────────────────────────────────────────────────────────
function selectSymptom(id, sym) {
  const slot = slots.find(s => s.id === id);
  if (!slot) return;

  slot.value = sym;
  const input = document.getElementById(`input-${id}`);
  input.value = formatLabel(sym);
  input.classList.add('has-value');

  const wrap = document.getElementById(`wrap-${id}`);
  wrap.classList.remove('open');

  // Refresh all open dropdowns to update disabled states
  document.querySelectorAll('.slot-input-wrap.open').forEach(w => {
    const wId = parseInt(w.id.replace('wrap-', ''));
    populateDropdown(wId, document.getElementById(`input-${wId}`)?.value || '');
  });
}

// ── Keyboard navigation ───────────────────────────────────────────────────────
function onKeydown(e, id) {
  const dropdown = document.getElementById(`dropdown-${id}`);
  const options = dropdown.querySelectorAll('.dropdown-option:not(.disabled)');
  const highlighted = dropdown.querySelector('.highlighted');
  let idx = Array.from(options).indexOf(highlighted);

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    if (idx < options.length - 1) {
      highlighted?.classList.remove('highlighted');
      options[idx + 1].classList.add('highlighted');
      options[idx + 1].scrollIntoView({ block: 'nearest' });
    }
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    if (idx > 0) {
      highlighted?.classList.remove('highlighted');
      options[idx - 1].classList.add('highlighted');
      options[idx - 1].scrollIntoView({ block: 'nearest' });
    }
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (highlighted) {
      selectSymptom(id, highlighted.dataset.value);
    }
  } else if (e.key === 'Escape') {
    document.getElementById(`wrap-${id}`)?.classList.remove('open');
  }
}

// ── Update Add button state ───────────────────────────────────────────────────
function updateAddBtn() {
  const btn = document.getElementById('addBtn');
  btn.disabled = slots.length >= MAX_SLOTS;
  btn.title = slots.length >= MAX_SLOTS ? 'Maximum 17 symptoms reached' : '';
}

// ── Clear all ─────────────────────────────────────────────────────────────────
function clearAll() {
  slots = [];
  document.getElementById('symptomSlots').innerHTML = '';
  hideResult();
  hideError();
  addSlot();
  updateAddBtn();
}

// ── Predict ───────────────────────────────────────────────────────────────────
async function predict() {
  hideError();
  hideResult();

  const selected = slots.filter(s => s.value).map(s => s.value);

  if (selected.length === 0) {
    showError('Please select at least one symptom.');
    return;
  }

  // Build payload — fill remaining with 'None'
  const payload = {};
  for (let i = 0; i < 17; i++) {
    payload[`Symptom_${i + 1}`] = selected[i] || 'None';
  }

  const btn = document.getElementById('predictBtn');
  btn.disabled = true;
  btn.classList.add('loading');
  btn.querySelector('.btn-text').textContent = 'Analyzing';

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Server error ${res.status}`);
    }

    const data = await res.json();
    showResult(data);

  } catch (err) {
    showError(err.message || 'Failed to connect to the server.');
  } finally {
    btn.disabled = false;
    btn.classList.remove('loading');
    btn.querySelector('.btn-text').textContent = 'Analyze';
  }
}

// ── Show / hide result ────────────────────────────────────────────────────────
function showResult(data) {
  const card = document.getElementById('resultCard');
  document.getElementById('resultDisease').textContent = data.disease;

  const list = document.getElementById('precautionsList');
  list.innerHTML = '';
  (data.precautions || []).forEach((p, i) => {
    const div = document.createElement('div');
    div.className = 'precaution-item';
    div.style.animationDelay = `${i * 80}ms`;
    div.textContent = formatLabel(p);
    list.appendChild(div);
  });

  card.classList.add('visible');
  card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResult() {
  document.getElementById('resultCard').classList.remove('visible');
}

function showError(msg) {
  const card = document.getElementById('errorCard');
  document.getElementById('errorMsg').textContent = msg;
  card.classList.add('visible');
}

function hideError() {
  document.getElementById('errorCard').classList.remove('visible');
}

// ── Close dropdowns on outside click ─────────────────────────────────────────
document.addEventListener('click', (e) => {
  if (!e.target.closest('.slot-input-wrap')) closeAll();
});

// ── Start ─────────────────────────────────────────────────────────────────────
init();
