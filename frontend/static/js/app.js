const API_BASE = "";
let selectedInterests = [];
let allFestivals = [];
let currentUser = null;
let leafletMap = null;

document.addEventListener("DOMContentLoaded", () => {
  checkUserSession();
  fetchFestivals();
  loadAnalyticsOverview();
  loadOrganizerOverview();
});

// Tab Switching
function switchTab(tab) {
  // Gating tabs based on logged-in roles (Member 3 Gating)
  if (tab === 'gov') {
    if (!currentUser || currentUser.role !== 'government') {
      showToast("Access Restricted", "Only Tourism Department Officials can access Gov Analytics. Please log in.");
      openAuthModal();
      return;
    }
  } else if (tab === 'organizer') {
    if (!currentUser || currentUser.role !== 'authority') {
      showToast("Access Restricted", "Only Festival Authorities can access Site Operations. Please log in.");
      openAuthModal();
      return;
    }
  }

  document.getElementById('view-tourist').classList.add('hidden');
  document.getElementById('view-gov').classList.add('hidden');
  document.getElementById('view-organizer').classList.add('hidden');

  document.getElementById('tab-btn-tourist').className = "px-4 py-2 rounded-xl transition-all flex items-center gap-2 text-slate-400 hover:text-white";
  document.getElementById('tab-btn-gov').className = "px-4 py-2 rounded-xl transition-all flex items-center gap-2 text-slate-400 hover:text-white";
  document.getElementById('tab-btn-organizer').className = "px-4 py-2 rounded-xl transition-all flex items-center gap-2 text-slate-400 hover:text-white";

  if (tab === 'tourist') {
    document.getElementById('view-tourist').classList.remove('hidden');
    document.getElementById('tab-btn-tourist').className = "px-4 py-2 rounded-xl transition-all flex items-center gap-2 btn-terracotta";
  } else if (tab === 'gov') {
    document.getElementById('view-gov').classList.remove('hidden');
    document.getElementById('tab-btn-gov').className = "px-4 py-2 rounded-xl transition-all flex items-center gap-2 btn-terracotta";
    initLeafletMap();
  } else if (tab === 'organizer') {
    document.getElementById('view-organizer').classList.remove('hidden');
    document.getElementById('tab-btn-organizer').className = "px-4 py-2 rounded-xl transition-all flex items-center gap-2 btn-terracotta";
    loadOrganizerOverview();
  }
}

// Fetch Festivals List
async function fetchFestivals() {
  try {
    let url = `${API_BASE}/festivals`;
    if (currentUser) {
      url += `?role=${currentUser.role}&username=${currentUser.username}`;
    }
    const res = await fetch(url);
    const json = await res.json();
    allFestivals = json.data || [];
    renderFestivalsGrid(allFestivals);
    
    // Refresh tables
    renderMyPublishedEvents();
    renderPendingGovApprovals();
  } catch (err) {
    console.error("Error fetching festivals:", err);
  }
}

function applyFilters() {
  const dist = document.getElementById('filter-district').value.toLowerCase();
  const cat = document.getElementById('filter-category').value.toLowerCase();

  const filtered = allFestivals.filter(f => {
    const matchesDist = !dist || (f.district && f.district.toLowerCase().includes(dist));
    const matchesCat = !cat || (f.category && f.category.toLowerCase().includes(cat));
    return matchesDist && matchesCat;
  });
  renderFestivalsGrid(filtered);
}

function getCategoryIcon(category) {
  const cat = (category || "").toLowerCase();
  if (cat.includes("royal") || cat.includes("state") || cat.includes("heritage")) return "🐘";
  if (cat.includes("folk") || cat.includes("sports")) return "🐂";
  if (cat.includes("spiritual") || cat.includes("temple")) return "🛕";
  return "🎭";
}

function renderFestivalsGrid(festivals) {
  const grid = document.getElementById('festivals-grid');
  document.getElementById('festival-count').innerText = festivals.length;
  grid.innerHTML = "";

  festivals.forEach(fest => {
    const imgUrl = (fest.images && fest.images.length > 0) 
      ? (typeof fest.images[0] === 'object' ? fest.images[0].url : fest.images[0])
      : (fest.image_url || "https://images.unsplash.com/photo-1600100397608-f010f443b749");

    const scoreBadge = fest.score ? `<span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold"><i class="fa-solid fa-bolt text-yellow-400"></i> ${fest.score}% Match</span>` : "";

    const icon = getCategoryIcon(fest.category);

    const card = `
      <div class="cultural-card rounded-2xl overflow-hidden flex flex-col group">
        <div class="relative h-48 overflow-hidden bg-slate-900">
          <img src="${imgUrl}" alt="${fest.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          <div class="absolute inset-0 bg-gradient-to-t from-[#181423] via-transparent to-transparent"></div>
          <div class="absolute top-3 left-3 flex gap-2">
            <span class="px-2.5 py-1 rounded-full bg-slate-950/80 text-mysuru-gold text-xs font-semibold border border-mysuru-gold/30">${icon} ${fest.district || 'Karnataka'}</span>
          </div>
          <div class="absolute top-3 right-3">
            ${scoreBadge}
          </div>
        </div>
        <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
          <div>
            <h3 class="text-lg font-bold font-heading text-white group-hover:text-mysuru-gold transition-colors">${fest.name}</h3>
            <p class="text-xs text-slate-300 mt-1 line-clamp-2">${fest.short_description || fest.description || 'Grand cultural heritage festival of Karnataka.'}</p>
          </div>
          <div class="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span><i class="fa-solid fa-users text-amber-400 mr-1"></i> ${(fest.expected_footfall || fest.footfall || 100000).toLocaleString()} visitors</span>
            <span class="text-slate-300 font-medium">${fest.category || 'Culture'}</span>
          </div>
          <div class="grid grid-cols-3 gap-2 pt-1">
            <button onclick="openTouristGuide('${fest.id || fest.name}')" class="py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 text-[11px] font-semibold transition-all flex items-center justify-center gap-1 border border-slate-700">
              <i class="fa-solid fa-book-open text-amber-400"></i> Guide
            </button>
            <button onclick="openFestivalDetail('${fest.id || fest.name}')" class="py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 text-[11px] font-semibold transition-all flex items-center justify-center gap-1 border border-slate-700">
              <i class="fa-solid fa-circle-info"></i> Details
            </button>
            <button onclick="openTripPlanner('${fest.id || 'mysuru-dasara'}')" class="py-2 rounded-xl btn-royal-gold text-[11px] font-bold transition-all flex items-center justify-center gap-1">
              <i class="fa-solid fa-compass"></i> Trip
            </button>
          </div>
        </div>
      </div>
    `;
    grid.innerHTML += card;
  });
}

// AI Interest Quiz
function toggleInterest(btn, tag) {
  if (selectedInterests.includes(tag)) {
    selectedInterests = selectedInterests.filter(t => t !== tag);
    btn.classList.remove('bg-mysuru-gold', 'text-slate-950', 'font-bold');
    btn.classList.add('bg-slate-900', 'text-slate-300');
  } else {
    selectedInterests.push(tag);
    btn.classList.add('bg-mysuru-gold', 'text-slate-950', 'font-bold');
    btn.classList.remove('bg-slate-900', 'text-slate-300');
  }
}

async function runAIRecommendation() {
  if (selectedInterests.length === 0) {
    showToast("Select Interests", "Please tap at least one interest tag.");
    return;
  }
  try {
    const res = await fetch(`${API_BASE}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ interests: selectedInterests })
    });
    const json = await res.json();
    const recs = json.recommendations || [];

    allFestivals.forEach(f => {
      const match = recs.find(r => r.name === f.name || String(r.festival_id) === String(f.id));
      f.score = match ? match.score : 0;
    });

    allFestivals.sort((a, b) => (b.score || 0) - (a.score || 0));
    renderFestivalsGrid(allFestivals);
    showToast("AI Recommendations Updated", `Calculated matches using TF-IDF & Cosine Similarity.`);
  } catch (err) {
    console.error("Recommendation error:", err);
  }
}

// AI Tourist Guide Modal (Step 5)
async function openTouristGuide(festId) {
  try {
    const res = await fetch(`${API_BASE}/tourist-guide/${festId}`);
    const guide = await res.json();

    const dos = (guide.cultural_etiquette && guide.cultural_etiquette.dos) ? guide.cultural_etiquette.dos : ["Respect temple customs", "Wear modest clothing"];
    const donts = (guide.cultural_etiquette && guide.cultural_etiquette.donts) ? guide.cultural_etiquette.donts : ["Do not litter", "Avoid flash photography near sacred areas"];

    document.getElementById('guide-modal-body').innerHTML = `
      <div class="space-y-5">
        <div class="border-b border-slate-800 pb-3">
          <span class="px-2.5 py-1 rounded-full bg-amber-500/20 text-mysuru-gold text-xs font-bold">📖 Interactive AI Tourist Guide</span>
          <h2 class="text-2xl font-extrabold font-heading text-white mt-2">${guide.name}</h2>
          <p class="text-xs text-slate-400">Best Time to Visit: <strong class="text-amber-300">${guide.best_time_to_visit}</strong></p>
        </div>

        <div class="space-y-3">
          <h4 class="text-xs font-bold text-mysuru-gold uppercase tracking-wider">What is this Festival & Why Celebrated?</h4>
          <p class="text-xs text-slate-300 leading-relaxed">${guide.what_is_it} ${guide.why_celebrated}</p>
        </div>

        <div class="space-y-3">
          <h4 class="text-xs font-bold text-amber-400 uppercase tracking-wider">What Tourists Will See & Experience:</h4>
          <ul class="list-disc list-inside text-xs text-slate-300 space-y-1">
            ${(guide.what_tourists_will_see || []).map(item => `<li>${item}</li>`).join('')}
          </ul>
        </div>

        <div class="space-y-3">
          <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Authentic Local Food Specialties:</h4>
          <div class="flex flex-wrap gap-2">
            ${(guide.local_food_recommendations || []).map(f => `<span class="px-3 py-1 rounded-xl bg-slate-900 text-emerald-300 border border-emerald-500/30 text-xs font-medium">🥘 ${f}</span>`).join('')}
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <div class="p-3.5 rounded-2xl bg-emerald-950/30 border border-emerald-500/30 text-xs space-y-1.5">
            <h5 class="font-bold text-emerald-400">✅ Do's for Visitors:</h5>
            <ul class="space-y-1 text-slate-300">
              ${dos.map(d => `<li>• ${d}</li>`).join('')}
            </ul>
          </div>
          <div class="p-3.5 rounded-2xl bg-red-950/30 border border-red-500/30 text-xs space-y-1.5">
            <h5 class="font-bold text-red-400">❌ Don'ts for Visitors:</h5>
            <ul class="space-y-1 text-slate-300">
              ${donts.map(d => `<li>• ${d}</li>`).join('')}
            </ul>
          </div>
        </div>
      </div>
    `;
    document.getElementById('modal-guide').classList.remove('hidden');
  } catch (err) {
    console.error("Guide error:", err);
  }
}

// Detail Modal
async function openFestivalDetail(festId) {
  try {
    const res = await fetch(`${API_BASE}/festivals/${festId}`);
    const fest = await res.json();

    const annRes = await fetch(`${API_BASE}/announcements/${festId}`);
    const annJson = await annRes.json();
    const announcements = annJson.announcements || [];

    let annHtml = announcements.map(a => `
      <div class="p-3 rounded-xl bg-amber-950/40 border border-amber-500/30 text-xs text-amber-200 space-y-1">
        <div class="flex justify-between font-bold">
          <span><i class="fa-solid fa-bullhorn text-amber-400"></i> Organizer Broadcast</span>
          <span class="text-[10px] text-slate-400">${a.created_at}</span>
        </div>
        <p>${a.message}</p>
      </div>
    `).join('') || `<p class="text-xs text-slate-500 italic">No announcements published yet.</p>`;

    document.getElementById('detail-modal-body').innerHTML = `
      <div class="space-y-5">
        <div>
          <span class="px-2.5 py-1 rounded-full bg-amber-500/20 text-mysuru-gold text-xs font-bold">${fest.category || 'Heritage'}</span>
          <h2 class="text-2xl font-extrabold font-heading text-white mt-2">${fest.name}</h2>
          <p class="text-xs text-slate-400">${fest.district} District • Timings: ${fest.timings || 'All Day'}</p>
        </div>

        <div class="space-y-3">
          <h4 class="text-xs font-bold text-mysuru-gold uppercase tracking-wider">Cultural Significance & History</h4>
          <p class="text-xs text-slate-300 leading-relaxed">${fest.cultural_significance || fest.short_description || fest.description}</p>
        </div>

        <div class="space-y-3">
          <h4 class="text-xs font-bold text-amber-400 uppercase tracking-wider">Live Organizer Broadcasts</h4>
          <div class="space-y-2 max-h-40 overflow-y-auto pr-1">
            ${annHtml}
          </div>
        </div>

        <div class="pt-4 border-t border-slate-800 flex justify-end gap-3">
          <button onclick="closeModal('modal-detail'); openTouristGuide('${fest.id || festId}')" class="px-4 py-2 rounded-xl bg-slate-800 text-slate-200 text-xs font-bold">
            <i class="fa-solid fa-book-open text-amber-400"></i> Open AI Guide
          </button>
          <button onclick="closeModal('modal-detail'); openTripPlanner('${fest.id || festId}')" class="px-6 py-2 rounded-xl btn-royal-gold text-xs font-bold">
            <i class="fa-solid fa-compass"></i> Plan Trip & Route
          </button>
        </div>
      </div>
    `;
    document.getElementById('modal-detail').classList.remove('hidden');
  } catch (err) {
    console.error("Detail error:", err);
  }
}

// Customizable Trip Planner Modal (Step 5)
function openTripPlanner(festId) {
  document.getElementById('trip-festival-id').value = festId;
  document.getElementById('modal-trip').classList.remove('hidden');
  calculateTripPlan();
}

async function calculateTripPlan() {
  const starting_city = document.getElementById('trip-origin').value;
  const festId = document.getElementById('trip-festival-id').value;
  const start_date = document.getElementById('trip-date').value;
  const people = parseInt(document.getElementById('trip-people').value) || 1;

  try {
    const res = await fetch(`${API_BASE}/travel-plan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        starting_city: starting_city,
        destination_festival: festId,
        start_date: start_date,
        number_of_people: people
      })
    });
    const plan = await res.json();

    const hotelRes = await fetch(`${API_BASE}/hotels/${festId}`);
    const hotelJson = await hotelRes.json();
    const hotels = hotelJson.hotels || [];

    let modesHtml = (plan.mode_comparisons || []).map(m => `
      <div class="cultural-card p-4 rounded-2xl space-y-2">
        <div class="flex justify-between items-center">
          <span class="font-bold text-sm text-white">${m.mode}</span>
          <span class="text-xs font-extrabold text-mysuru-gold">${m.estimated_cost_per_person || m.estimated_cost}/person</span>
        </div>
        <div class="text-xs text-slate-400 flex justify-between">
          <span>Duration: ${m.duration}</span>
          <span>Haversine Dist: ${m.distance_km} km</span>
        </div>
        <div class="text-xs text-emerald-400 font-bold">Total Group (${people} travelers): ${m.total_group_cost || m.estimated_cost}</div>
      </div>
    `).join('');

    let itinerary = plan.itinerary || {};
    let day1 = itinerary.day1 || {};
    let day2 = itinerary.day2 || {};

    let hotelsHtml = hotels.map(h => `
      <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
        <div>
          <h5 class="font-bold text-xs text-white">${h.name}</h5>
          <p class="text-[11px] text-slate-400">${h.distance_km} km away • ${h.rating}</p>
        </div>
        <div class="text-right">
          <span class="text-xs font-bold text-emerald-400 block">${h.price_per_night}</span>
          <a href="${h.booking_url}" target="_blank" class="text-[10px] text-mysuru-gold hover:underline">Book Now <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
        </div>
      </div>
    `).join('');

    document.getElementById('trip-modal-output').innerHTML = `
      <div class="space-y-5">
        <div>
          <h4 class="text-xs font-bold text-mysuru-gold uppercase tracking-wider">Haversine Distance & Transit Comparisons (${starting_city} ➔ ${plan.destination_festival})</h4>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-2">
            ${modesHtml}
          </div>
        </div>

        <div>
          <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Structured 2-Day Travel Itinerary</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
            <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
              <h5 class="font-bold text-xs text-mysuru-gold">Day 1: ${day1.title || 'Arrival'}</h5>
              <ul class="space-y-1.5 text-[11px] text-slate-300">
                ${(day1.schedule || []).map(s => `<li><strong class="text-slate-400">${s.time}:</strong> ${s.activity}</li>`).join('')}
              </ul>
            </div>
            <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
              <h5 class="font-bold text-xs text-amber-400">Day 2: ${day2.title || 'Return'}</h5>
              <ul class="space-y-1.5 text-[11px] text-slate-300">
                ${(day2.schedule || []).map(s => `<li><strong class="text-slate-400">${s.time}:</strong> ${s.activity}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>

        <div>
          <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Nearby Hotel Accommodations</h4>
          <div class="space-y-2 mt-2">
            ${hotelsHtml}
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    console.error("Trip plan error:", err);
  }
}

// Leaflet GIS OpenStreetMap Map Integration (Step 2)
async function initLeafletMap() {
  if (leafletMap) return;

  leafletMap = L.map('map').setView([14.25, 75.8], 7);

  // OpenStreetMap Dark Tile Layer (No Paid Keys Required)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
  }).addTo(leafletMap);

  try {
    const res = await fetch(`${API_BASE}/analytics/map-data`);
    const json = await res.json();
    const features = json.features || [];
    const advList = document.getElementById('advisory-list');
    advList.innerHTML = "";

    features.forEach(feat => {
      const props = feat.properties;
      const coords = feat.geometry.coordinates; // [lng, lat]
      const color = props.risk_color || "#FAAD14";

      const marker = L.circleMarker([coords[1], coords[0]], {
        radius: 10,
        fillColor: color,
        color: "#fff",
        weight: 1.5,
        fillOpacity: 0.85
      }).addTo(leafletMap);

      const popupContent = `
        <div class="space-y-1">
          <h4 class="font-bold text-sm text-white">${props.name}</h4>
          <p class="text-xs text-slate-300">${props.district} • Footfall: <strong>${(props.predicted_footfall).toLocaleString()}</strong></p>
          <div class="pt-1 text-[11px] text-amber-300">
            <strong>Advisory:</strong> ${props.infrastructure_advisories ? props.infrastructure_advisories.transport : 'Standard logistics'}
          </div>
        </div>
      `;
      marker.bindPopup(popupContent);

      advList.innerHTML += `
        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div class="flex justify-between items-center font-bold">
            <span class="text-slate-200">${props.name}</span>
            <span class="text-[10px] px-2 py-0.5 rounded" style="background:${color}20; color:${color}">${props.risk_badge}</span>
          </div>
          <p class="text-[11px] text-slate-400"><strong>Transport:</strong> ${props.infrastructure_advisories.transport}</p>
          <p class="text-[11px] text-slate-400"><strong>Sanitation:</strong> ${props.infrastructure_advisories.sanitation}</p>
        </div>
      `;
    });
  } catch (err) {
    console.error("Map error:", err);
  }
}

// Gov Analytics
async function loadAnalyticsOverview() {
  try {
    const res = await fetch(`${API_BASE}/analytics/overview`);
    const ov = await res.json();
    document.getElementById('kpi-total-festivals').innerText = ov.total_festivals;
    document.getElementById('kpi-expected-visitors').innerText = ov.formatted_visitors;
    document.getElementById('kpi-high-risk').innerText = ov.high_risk_events_count;
    document.getElementById('kpi-trending').innerText = ov.trending_district;

    const trendsRes = await fetch(`${API_BASE}/analytics/trends`);
    const trends = await trendsRes.json();
    const trendsContainer = document.getElementById('trends-container');

    let distHtml = (trends.district_distribution || []).slice(0, 5).map(d => `
      <div class="space-y-1">
        <div class="flex justify-between text-xs font-semibold">
          <span class="text-slate-300">${d.district}</span>
          <span class="text-mysuru-gold">${(d.footfall / 1000).toFixed(0)}k</span>
        </div>
        <div class="w-full bg-slate-900 rounded-full h-2">
          <div class="bg-mysuru-gold h-2 rounded-full" style="width: ${Math.min(100, (d.footfall / 2000000) * 100)}%"></div>
        </div>
      </div>
    `).join('');

    trendsContainer.innerHTML = `
      <div class="space-y-3 col-span-2">
        <h4 class="text-xs font-bold text-slate-400 uppercase">Top Karnataka District Footfall Shares</h4>
        ${distHtml}
      </div>
    `;
  } catch (err) {
    console.error("Analytics overview error:", err);
  }
}

// Site Ops Overview & Event Publishing (Step 4)
async function loadOrganizerOverview() {
  const festId = document.getElementById('organizer-fest-select').value;
  try {
    const res = await fetch(`${API_BASE}/organizer/overview/${festId}`);
    const ops = await res.json();

    const count = ops.realtime_visitor_estimate || ops.current_visitors || 142000;
    const pct = ops.crowd_occupancy_percentage || "71.0%";

    document.getElementById('ops-visitor-count').innerText = count.toLocaleString();
    document.getElementById('ops-occupancy-pct').innerText = pct;
    document.getElementById('ops-occupancy-bar').style.width = pct;

    const flags = ops.warning_flags || [];
    document.getElementById('ops-warning-flags').innerHTML = flags.map(f => `<li>• ${f}</li>`).join('');
  } catch (err) {
    console.error("Organizer ops error:", err);
  }
}

// User Session & Header Management (Member 3 Auth Control)
function checkUserSession() {
  const session = localStorage.getItem("sanskriti_session");
  const overlay = document.getElementById("welcome-overlay");
  if (session) {
    try {
      currentUser = JSON.parse(session);
      updateAuthHeaderUI();
      if (overlay) overlay.classList.add("hidden");
    } catch (e) {
      localStorage.removeItem("sanskriti_session");
      if (overlay) overlay.classList.remove("hidden");
    }
  } else {
    if (overlay) overlay.classList.remove("hidden");
  }
}

// Welcome Overlay Auth Screen Controls
let currentWelcomeTab = 'login';

function toggleWelcomeTab(tab) {
  currentWelcomeTab = tab;
  const loginBtn = document.getElementById("welcome-tab-login");
  const signupBtn = document.getElementById("welcome-tab-signup");
  const roleWrapper = document.getElementById("welcome-role-wrapper");
  const extraFields = document.getElementById("welcome-signup-fields-wrapper");
  const submitBtn = document.getElementById("welcome-submit-btn");

  if (tab === 'login') {
    loginBtn.className = "flex-1 py-1.5 rounded-lg bg-mysuru-gold text-slate-950";
    signupBtn.className = "flex-1 py-1.5 rounded-lg text-slate-400 hover:text-white";
    roleWrapper.classList.add("hidden");
    if (extraFields) extraFields.classList.add("hidden");
    submitBtn.innerHTML = `<i class="fa-solid fa-unlock-keyhole"></i> <span>Log In & Enter Portal</span>`;
  } else {
    signupBtn.className = "flex-1 py-1.5 rounded-lg bg-mysuru-gold text-slate-950";
    loginBtn.className = "flex-1 py-1.5 rounded-lg text-slate-400 hover:text-white";
    roleWrapper.classList.remove("hidden");
    if (extraFields) extraFields.classList.remove("hidden");
    submitBtn.innerHTML = `<i class="fa-solid fa-user-plus"></i> <span>Create Account & Enter</span>`;
  }
}

async function submitWelcomeAuthForm() {
  const username = document.getElementById("welcome-username").value.trim();
  const password = document.getElementById("welcome-password").value.trim();
  const role = document.getElementById("welcome-role").value;
  
  let email = null;
  let phone = null;
  const emailInput = document.getElementById("welcome-email");
  const phoneInput = document.getElementById("welcome-phone");
  if (emailInput) email = emailInput.value.trim();
  if (phoneInput) phone = phoneInput.value.trim();

  if (!username || !password) {
    showToast("Input Required", "Please enter both username and password.");
    return;
  }

  const endpoint = currentWelcomeTab === 'login' ? '/auth/login' : '/auth/register';
  const payload = { username, password };
  if (currentWelcomeTab === 'signup') {
    payload.role = role;
    payload.email = email;
    payload.phone = phone;
  }

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const err = await res.json();
      showToast("Auth Failed", err.detail || "Authentication request failed.");
      return;
    }

    const data = await res.json();
    
    if (currentWelcomeTab === 'login') {
      currentUser = {
        username: data.user.username,
        role: data.user.role,
        name: data.user.name,
        token: data.token
      };
      localStorage.setItem("sanskriti_session", JSON.stringify(currentUser));
      
      const overlay = document.getElementById("welcome-overlay");
      if (overlay) overlay.classList.add("hidden");
      
      showToast("Authentication Successful", `Welcome, ${currentUser.name}!`);
      
      // Clean inputs
      document.getElementById("welcome-username").value = "";
      document.getElementById("welcome-password").value = "";

      updateAuthHeaderUI();
      // Redirect based on role
      if (currentUser.role === 'government') {
        switchTab('gov');
      } else if (currentUser.role === 'authority') {
        switchTab('organizer');
      } else {
        switchTab('tourist');
      }
      fetchFestivals();
    } else {
      showToast("Account Created", "Successfully registered! Welcome SMS & Email sent.");
      toggleWelcomeTab('login');
      document.getElementById("welcome-username").value = username;
      document.getElementById("welcome-password").value = "";
    }
  } catch (err) {
    console.error("Welcome auth error:", err);
    showToast("Server Connection Error", "Unable to connect to auth server.");
  }
}

function dismissWelcomeOverlay() {
  const overlay = document.getElementById("welcome-overlay");
  if (overlay) overlay.classList.add("hidden");
  showToast("Welcome Guest", "You are exploring the tourist discovery feed in read-only mode.");
  switchTab('tourist');
}

function updateAuthHeaderUI() {
  const authDiv = document.getElementById("auth-controls");
  if (!authDiv) return;

  if (currentUser) {
    let roleText = currentUser.role.toUpperCase();
    if (roleText === "AUTHORITY") roleText = "Authority";
    if (roleText === "GOVERNMENT") roleText = "Dept Official";
    if (roleText === "TOURIST") roleText = "Tourist";
    
    authDiv.innerHTML = `
      <div class="flex items-center gap-2">
        <span class="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[10px] text-slate-300 font-bold">
          <i class="fa-solid fa-user-circle text-[#D4AF37] mr-1"></i> ${currentUser.name} (${roleText})
        </span>
        <button onclick="logout()" class="px-2.5 py-1.5 rounded-lg bg-red-950/40 text-red-400 hover:text-red-300 border border-red-500/20 text-xs flex items-center gap-1 font-bold">
          <i class="fa-solid fa-right-from-bracket"></i> <span>Log Out</span>
        </button>
      </div>
    `;
  } else {
    authDiv.innerHTML = `
      <button onclick="openAuthModal()" class="px-4 py-2 rounded-xl btn-royal-gold text-xs flex items-center gap-1.5">
        <i class="fa-solid fa-user-lock"></i> <span>Login / Sign Up</span>
      </button>
    `;
  }
  
  // Refresh grids and tables
  renderMyPublishedEvents();
  renderPendingGovApprovals();
}

function logout() {
  currentUser = null;
  localStorage.removeItem("sanskriti_session");
  updateAuthHeaderUI();
  
  // Show welcome overlay again
  const overlay = document.getElementById("welcome-overlay");
  if (overlay) overlay.classList.remove("hidden");

  showToast("Logged Out", "You have successfully logged out of the portal.");
  switchTab("tourist");
  fetchFestivals();
}

// Authentication Modal UI Handlers
let currentAuthTab = 'login';

function openAuthModal() {
  document.getElementById("modal-auth").classList.remove("hidden");
  toggleAuthTab('login');
}

function toggleAuthTab(tab) {
  currentAuthTab = tab;
  const loginBtn = document.getElementById("auth-tab-login");
  const signupBtn = document.getElementById("auth-tab-signup");
  const roleWrapper = document.getElementById("auth-role-wrapper");
  const extraFields = document.getElementById("auth-signup-fields-wrapper");
  const submitBtn = document.getElementById("auth-submit-btn");

  if (tab === 'login') {
    loginBtn.className = "flex-1 py-1.5 rounded-lg bg-mysuru-gold text-slate-950";
    signupBtn.className = "flex-1 py-1.5 rounded-lg text-slate-400 hover:text-white";
    roleWrapper.classList.add("hidden");
    if (extraFields) extraFields.classList.add("hidden");
    submitBtn.innerHTML = `<i class="fa-solid fa-unlock-keyhole"></i> <span>Log In to Account</span>`;
  } else {
    signupBtn.className = "flex-1 py-1.5 rounded-lg bg-mysuru-gold text-slate-950";
    loginBtn.className = "flex-1 py-1.5 rounded-lg text-slate-400 hover:text-white";
    roleWrapper.classList.remove("hidden");
    if (extraFields) extraFields.classList.remove("hidden");
    submitBtn.innerHTML = `<i class="fa-solid fa-user-plus"></i> <span>Create Account</span>`;
  }
}

async function submitAuthForm() {
  const username = document.getElementById("auth-username").value.trim();
  const password = document.getElementById("auth-password").value.trim();
  const role = document.getElementById("auth-role").value;
  
  let email = null;
  let phone = null;
  const emailInput = document.getElementById("auth-email");
  const phoneInput = document.getElementById("auth-phone");
  if (emailInput) email = emailInput.value.trim();
  if (phoneInput) phone = phoneInput.value.trim();

  if (!username || !password) {
    showToast("Input Required", "Please enter both username and password.");
    return;
  }

  const endpoint = currentAuthTab === 'login' ? '/auth/login' : '/auth/register';
  const payload = { username, password };
  if (currentAuthTab === 'signup') {
    payload.role = role;
    payload.email = email;
    payload.phone = phone;
  }

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const err = await res.json();
      showToast("Auth Failed", err.detail || "Authentication request failed.");
      return;
    }

    const data = await res.json();
    
    if (currentAuthTab === 'login') {
      currentUser = {
        username: data.user.username,
        role: data.user.role,
        name: data.user.name,
        token: data.token
      };
      localStorage.setItem("sanskriti_session", JSON.stringify(currentUser));
      closeModal('modal-auth');
      showToast("Authentication Successful", `Welcome, ${currentUser.name}!`);
      
      // Clean inputs
      document.getElementById("auth-username").value = "";
      document.getElementById("auth-password").value = "";

      updateAuthHeaderUI();
      // Redirect based on role
      if (currentUser.role === 'government') {
        switchTab('gov');
      } else if (currentUser.role === 'authority') {
        switchTab('organizer');
      } else {
        switchTab('tourist');
      }
      fetchFestivals();
    } else {
      showToast("Account Created", "Successfully registered! Welcome SMS & Email sent.");
      toggleAuthTab('login');
      document.getElementById("auth-username").value = username;
      document.getElementById("auth-password").value = "";
    }
  } catch (err) {
    console.error("Auth error:", err);
    showToast("Server Connection Error", "Unable to connect to auth server.");
  }
}

// Publish New Festival (Member 3 / Site Ops)
async function publishNewOrganizerEvent() {
  const name = document.getElementById("pub-name").value.trim();
  const district = document.getElementById("pub-district").value.trim();
  const city = document.getElementById("pub-city").value.trim();
  const start_date = document.getElementById("pub-start-date").value;
  const end_date = document.getElementById("pub-end-date").value;
  const category = document.getElementById("pub-category").value.trim();
  const expected_footfall = parseInt(document.getElementById("pub-footfall").value) || 10000;
  const latitude = parseFloat(document.getElementById("pub-latitude").value) || 12.9716;
  const longitude = parseFloat(document.getElementById("pub-longitude").value) || 77.5946;
  const image_url = document.getElementById("pub-image-url").value.trim();
  const short_description = document.getElementById("pub-desc").value.trim();
  const cultural_significance = document.getElementById("pub-significance").value.trim();
  const attractions = document.getElementById("pub-attractions").value.split(",").map(x => x.trim()).filter(Boolean);
  const food = document.getElementById("pub-food").value.split(",").map(x => x.trim()).filter(Boolean);
  const activities = document.getElementById("pub-activities").value.split(",").map(x => x.trim()).filter(Boolean);

  if (!name) {
    showToast("Input Required", "Please enter the festival name.");
    return;
  }

  const payload = {
    name, district, city, start_date, end_date, category,
    expected_footfall, latitude, longitude, image_url,
    short_description, cultural_significance,
    major_attractions: attractions, local_food: food, activities,
    owner_username: currentUser ? currentUser.username : "authority1"
  };

  try {
    const res = await fetch(`${API_BASE}/organizer/publish-festival`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      showToast("Publishing Failed", "Could not submit event details.");
      return;
    }

    showToast("Submission Sent!", "Your event is pending verification by the Tourism Department.");
    closeModal("modal-publish");
    fetchFestivals();
  } catch (err) {
    console.error("Publish error:", err);
    showToast("Publishing Error", "Server connection timed out.");
  }
}

// Render "My Published Events" Table (Member 3 Control Panel)
function renderMyPublishedEvents() {
  const tbody = document.getElementById("my-festivals-list");
  if (!tbody) return;
  
  tbody.innerHTML = "";
  if (!currentUser || currentUser.role !== 'authority') {
    tbody.innerHTML = `<tr><td colspan="6" class="py-4 text-center text-slate-500 italic">Please log in as a Festival Authority to view your events.</td></tr>`;
    return;
  }

  const myEvents = allFestivals.filter(f => f.owner_username === currentUser.username);
  if (myEvents.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="py-4 text-center text-slate-500 italic">No events published yet. Click "Publish New Event" to get started!</td></tr>`;
    return;
  }

  myEvents.forEach(f => {
    const f_id = f.id || f.festival_id;
    const status = f.verification_status || "pending";
    
    let statusBadge = "";
    if (status === "approved") {
      statusBadge = `<span class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold">Approved</span>`;
    } else if (status === "rejected") {
      statusBadge = `<span class="px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/30 text-[10px] font-bold">Rejected</span>`;
    } else {
      statusBadge = `<span class="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold">Pending Review</span>`;
    }

    tbody.innerHTML += `
      <tr class="hover:bg-slate-900/40 border-b border-slate-800/40">
        <td class="py-3 px-3 font-semibold text-white">${f.name}</td>
        <td class="py-3 px-3">${f.district}${f.city ? `, ${f.city}` : ""}</td>
        <td class="py-3 px-3">${f.category || "General"}</td>
        <td class="py-3 px-3">${(f.expected_footfall || 0).toLocaleString()}</td>
        <td class="py-3 px-3">${statusBadge}</td>
        <td class="py-3 px-3 text-right space-x-1 whitespace-nowrap">
          <button onclick="openEditFestival('${f_id}')" class="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:border-mysuru-gold/40 text-slate-300 hover:text-white transition-all text-[11px] font-semibold">
            <i class="fa-solid fa-pen text-[9px]"></i> Edit
          </button>
          <button onclick="deleteFestival('${f_id}')" class="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:border-red-500/40 text-red-400 hover:text-red-300 transition-all text-[11px] font-semibold">
            <i class="fa-solid fa-trash text-[9px]"></i> Delete
          </button>
        </td>
      </tr>
    `;
  });
}

// Edit Festival Event
function openEditFestival(festId) {
  const f = allFestivals.find(x => String(x.id || x.festival_id) === String(festId));
  if (!f) return;

  document.getElementById("edit-id").value = festId;
  document.getElementById("edit-name").value = f.name || "";
  document.getElementById("edit-district").value = f.district || "";
  document.getElementById("edit-city").value = f.city || "";
  document.getElementById("edit-start-date").value = f.start_date || "";
  document.getElementById("edit-end-date").value = f.end_date || "";
  document.getElementById("edit-category").value = f.category || "";
  document.getElementById("edit-footfall").value = f.expected_footfall || 10000;
  document.getElementById("edit-latitude").value = f.latitude || 12.9716;
  document.getElementById("edit-longitude").value = f.longitude || 77.5946;
  
  const imgUrl = (f.images && f.images.length > 0) 
    ? (typeof f.images[0] === 'object' ? f.images[0].url : f.images[0])
    : (f.image_url || "");
  document.getElementById("edit-image-url").value = imgUrl;
  
  document.getElementById("edit-desc").value = f.short_description || f.description || "";
  document.getElementById("edit-significance").value = f.cultural_significance || "";
  document.getElementById("edit-attractions").value = Array.isArray(f.major_attractions) ? f.major_attractions.join(", ") : (f.major_attractions || "");
  document.getElementById("edit-food").value = Array.isArray(f.local_food) ? f.local_food.join(", ") : (f.local_food || "");
  document.getElementById("edit-activities").value = Array.isArray(f.activities) ? f.activities.join(", ") : (f.activities || "");

  document.getElementById("modal-edit").classList.remove("hidden");
}

async function submitEditFestival() {
  const id = document.getElementById("edit-id").value;
  const name = document.getElementById("edit-name").value.trim();
  const district = document.getElementById("edit-district").value.trim();
  const city = document.getElementById("edit-city").value.trim();
  const start_date = document.getElementById("edit-start-date").value;
  const end_date = document.getElementById("edit-end-date").value;
  const category = document.getElementById("edit-category").value.trim();
  const expected_footfall = parseInt(document.getElementById("edit-footfall").value) || 10000;
  const latitude = parseFloat(document.getElementById("edit-latitude").value) || 12.9716;
  const longitude = parseFloat(document.getElementById("edit-longitude").value) || 77.5946;
  const image_url = document.getElementById("edit-image-url").value.trim();
  const short_description = document.getElementById("edit-desc").value.trim();
  const cultural_significance = document.getElementById("edit-significance").value.trim();
  const attractions = document.getElementById("edit-attractions").value.split(",").map(x => x.trim()).filter(Boolean);
  const food = document.getElementById("edit-food").value.split(",").map(x => x.trim()).filter(Boolean);
  const activities = document.getElementById("edit-activities").value.split(",").map(x => x.trim()).filter(Boolean);

  const payload = {
    name, district, city, start_date, end_date, category,
    expected_footfall, latitude, longitude, image_url,
    short_description, cultural_significance,
    major_attractions: attractions, local_food: food, activities
  };

  try {
    const res = await fetch(`${API_BASE}/organizer/update-festival/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      showToast("Update Failed", "Could not save festival updates.");
      return;
    }

    showToast("Event Updated", "Festival details successfully modified.");
    closeModal("modal-edit");
    fetchFestivals();
  } catch (err) {
    console.error("Update error:", err);
    showToast("Update Error", "Connection timed out.");
  }
}

// Delete / Unpublish Festival
async function deleteFestival(festId) {
  if (!confirm("Are you sure you want to delete and unpublish this festival? This action cannot be undone.")) return;
  
  try {
    let url = `${API_BASE}/organizer/delete-festival/${festId}`;
    if (currentUser) {
      url += `?username=${currentUser.username}`;
    }
    const res = await fetch(url, { method: "DELETE" });
    
    if (!res.ok) {
      showToast("Deletion Failed", "Not authorized or event does not exist.");
      return;
    }

    showToast("Event Deleted", "Successfully removed from dashboard feeds.");
    fetchFestivals();
  } catch (err) {
    console.error("Delete error:", err);
    showToast("Delete Error", "Could not connect to database.");
  }
}

// Render Tourism Department Pending Verifications
function renderPendingGovApprovals() {
  const tbody = document.getElementById("gov-pending-list");
  if (!tbody) return;

  tbody.innerHTML = "";
  if (!currentUser || currentUser.role !== 'government') {
    tbody.innerHTML = `<tr><td colspan="6" class="py-4 text-center text-slate-500 italic">Please log in as a Tourism Department Officer to access approvals.</td></tr>`;
    return;
  }

  const pendingEvents = allFestivals.filter(f => !f.verified || f.verification_status === "pending");
  if (pendingEvents.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="py-4 text-center text-emerald-400 font-bold"><i class="fa-solid fa-check-circle mr-1"></i> Verification Inbox Clean! All events are approved.</td></tr>`;
    return;
  }

  pendingEvents.forEach(f => {
    const f_id = f.id || f.festival_id;
    const publisher = f.owner_username || "anonymous";
    const desc = f.short_description || f.description || "No description provided.";

    tbody.innerHTML += `
      <tr class="hover:bg-slate-900/40 border-b border-slate-800/40">
        <td class="py-3 px-3 font-semibold text-white">${f.name}</td>
        <td class="py-3 px-3">${f.district}${f.city ? `, ${f.city}` : ""}</td>
        <td class="py-3 px-3">${f.category || "General"}</td>
        <td class="py-3 px-3"><span class="px-2 py-0.5 rounded bg-slate-950 font-mono text-[10px] text-slate-400">${publisher}</span></td>
        <td class="py-3 px-3 max-w-[200px] truncate" title="${desc}">${desc}</td>
        <td class="py-3 px-3 text-right space-x-1 whitespace-nowrap">
          <button onclick="verifyEvent('${f_id}', 'approve')" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition-all shadow-md shadow-emerald-600/20 text-[11px]">
            <i class="fa-solid fa-check text-[10px]"></i> Approve
          </button>
          <button onclick="verifyEvent('${f_id}', 'reject')" class="px-2.5 py-1 rounded-lg bg-red-600 hover:bg-red-500 text-white font-bold transition-all shadow-md shadow-red-600/20 text-[11px]">
            <i class="fa-solid fa-xmark text-[10px]"></i> Reject
          </button>
        </td>
      </tr>
    `;
  });
}

async function verifyEvent(festId, action) {
  try {
    const res = await fetch(`${API_BASE}/gov/verify-festival/${festId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action })
    });

    if (!res.ok) {
      showToast("Action Failed", "Could not complete verification state change.");
      return;
    }

    const state = action === "approve" ? "Approved" : "Rejected";
    showToast(`Event ${state}`, `The festival is now officially marked as ${state.toLowerCase()}.`);
    fetchFestivals();
  } catch (err) {
    console.error("Verify error:", err);
    showToast("Verify Error", "Could not complete request.");
  }
}

// Multilingual Translation Toggle
async function setLanguage(lang) {
  document.getElementById('lang-en').className = lang === 'en' ? "px-2.5 py-1 rounded-lg bg-mysuru-gold text-slate-950 font-bold" : "px-2.5 py-1 rounded-lg text-slate-400 hover:text-white";
  document.getElementById('lang-kn').className = lang === 'kn' ? "px-2.5 py-1 rounded-lg bg-mysuru-gold text-slate-950 font-bold" : "px-2.5 py-1 rounded-lg text-slate-400 hover:text-white";
  document.getElementById('lang-hi').className = lang === 'hi' ? "px-2.5 py-1 rounded-lg bg-mysuru-gold text-slate-950 font-bold" : "px-2.5 py-1 rounded-lg text-slate-400 hover:text-white";

  if (lang === 'en') {
    document.getElementById('hero-heading').innerText = "Discover Karnataka's Living Traditions & Grand Festivals";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/translate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: "Discover Karnataka's Living Traditions & Grand Festivals", target_lang: lang })
    });
    const json = await res.json();
    document.getElementById('hero-heading').innerText = json.translated_text;
  } catch (err) {
    console.error("Translation error:", err);
  }
}

function closeModal(id) {
  document.getElementById(id).classList.add('hidden');
}

function showToast(title, msg) {
  const banner = document.getElementById('toast-banner');
  if (!banner) return;
  document.getElementById('toast-title').innerText = title;
  document.getElementById('toast-body').innerText = msg;
  banner.classList.remove('hidden');
  setTimeout(() => banner.classList.add('hidden'), 4000);
}
