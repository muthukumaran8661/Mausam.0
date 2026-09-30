/**
 * Mausam Client-Side Application Logic
 * Mobile-first reactive controller with dynamic theming, i18n, and offline handling.
 */

(function () {
  'use strict';

  // --- Localization Dictionary ---
  const TRANSLATIONS = {
    en: {
      goodMorning: "Good morning,",
      goodAfternoon: "Good afternoon,",
      goodEvening: "Good evening,",
      goodNight: "Good night,",
      smartInsights: "Personalized Insights",
      viewAll: "View All",
      hourlyForecast: "Hourly Forecast",
      next24h: "Next 24 Hours",
      sevenDayForecast: "7-Day Forecast",
      keyMetrics: "Key Metrics",
      humidity: "Humidity",
      wind: "Wind",
      uvIndex: "UV Index",
      aqi: "Air Quality",
      visibility: "Visibility",
      pressure: "Pressure",
      sunCycle: "Sun Cycle",
      sunrise: "Sunrise",
      sunset: "Sunset",
      savedCities: "Saved Cities",
      addCity: "+ Add City",
      navHome: "Home",
      navForecast: "Forecast",
      navMap: "Map",
      navCities: "Cities",
      navProfile: "Profile",
      allInsightsTitle: "All Smart Insights",
      searchCityTitle: "Search Location",
      settingsTitle: "Preferences & Profile",
      tempUnits: "Temperature Units",
      appLanguage: "Language",
      lifestyleInterests: "Lifestyle Interests",
      weatherSensitivities: "Sensitivities",
      commuteTimes: "Daily Commute Times",
      morningCommute: "Morning",
      eveningCommute: "Evening",
      savePreferences: "Save Preferences",
      offlineText: "📡 Offline Mode — Showing cached weather",
      retry: "Retry"
    },
    hi: {
      goodMorning: "शुभ प्रभात,",
      goodAfternoon: "नमस्ते,",
      goodEvening: "शुभ संध्या,",
      goodNight: "शुभ रात्रि,",
      smartInsights: "स्मार्ट व्यक्तिगत सुझाव",
      viewAll: "सभी देखें",
      hourlyForecast: "प्रति घंटा पूर्वानुमान",
      next24h: "अगले 24 घंटे",
      sevenDayForecast: "7-दिवसीय पूर्वानुमान",
      keyMetrics: "मुख्य मौसम संकेतक",
      humidity: "आर्द्रता (नमी)",
      wind: "हवा की गति",
      uvIndex: "पराबैंगनी (UV)",
      aqi: "वायु गुणवत्ता (AQI)",
      visibility: "दृश्यता",
      pressure: "वायुमंडलीय दबाव",
      sunCycle: "सूर्योदय / सूर्यास्त",
      sunrise: "सूर्योदय",
      sunset: "सूर्यास्त",
      savedCities: "सहेजे गए शहर",
      addCity: "+ शहर जोड़ें",
      navHome: "होम",
      navForecast: "पूर्वानुमान",
      navMap: "नक्शा",
      navCities: "शहर",
      navProfile: "प्रोफ़ाइल",
      allInsightsTitle: "सभी व्यक्तिगत सुझाव",
      searchCityTitle: "शहर खोजें",
      settingsTitle: "प्राथमिकताएं और सेटिंग्स",
      tempUnits: "तापमान इकाई",
      appLanguage: "भाषा",
      lifestyleInterests: "दैनिक रुचियां",
      weatherSensitivities: "मौसम संवेदनशीलता",
      commuteTimes: "आवागमन (कम्यूट) समय",
      morningCommute: "सुबह",
      eveningCommute: "शाम",
      savePreferences: "प्राथमिकताएं सहेजें",
      offlineText: "📡 ऑफ़लाइन मोड — कैश्ड मौसम दिखाया जा रहा है",
      retry: "पुनः प्रयास"
    },
    ta: {
      goodMorning: "காலை வணக்கம்,",
      goodAfternoon: "மதிய வணக்கம்,",
      goodEvening: "மாலை வணக்கம்,",
      goodNight: "இரவு வணக்கம்,",
      smartInsights: "தனிப்பயனாக்கப்பட்ட குறிப்புகள்",
      viewAll: "அனைத்தும்",
      hourlyForecast: "மணிநேர முன்னறிவிப்பு",
      next24h: "அடுத்த 24 மணிநேரம்",
      sevenDayForecast: "7-நாள் வானிலை",
      keyMetrics: "முக்கிய அளவீடுகள்",
      humidity: "ஈரப்பதம்",
      wind: "காற்று வேகம்",
      uvIndex: "புற ஊதா (UV)",
      aqi: "காற்று தரம் (AQI)",
      visibility: "பார்வை தூரம்",
      pressure: "வளிமண்டல அழுத்தம்",
      sunCycle: "சூரிய சுழற்சி",
      sunrise: "சூரிய உதயம்",
      sunset: "சூரிய அஸ்தமனம்",
      savedCities: "சேமிக்கப்பட்ட நகரங்கள்",
      addCity: "+ நகரம் சேர்",
      navHome: "முகப்பு",
      navForecast: "வானிலை",
      navMap: "வரைபடம்",
      navCities: "நகரங்கள்",
      navProfile: "சுயவிவரம்",
      allInsightsTitle: "அனைத்து வானிலை குறிப்புகள்",
      searchCityTitle: "நகரத்தைத் தேடுங்கள்",
      settingsTitle: "விருப்பத்தேர்வுகள்",
      tempUnits: "வெப்பநிலை அலகுகள்",
      appLanguage: "மொழி",
      lifestyleInterests: "வாழ்க்கை முறை ஆர்வங்கள்",
      weatherSensitivities: "உணர்திறன் அமைப்புகள்",
      commuteTimes: "பயண நேரங்கள்",
      morningCommute: "காலை",
      eveningCommute: "மாலை",
      savePreferences: "அமைப்புகளைச் சேமி",
      offlineText: "📡 ஆஃப்லைன் பயன்முறை — சேமிக்கப்பட்ட வானிலை",
      retry: "மீண்டும் முயல்க"
    }
  };

  // --- App State ---
  const state = {
    userId: 1,
    userName: "Rahul",
    language: "en",
    units: "metric",
    currentLocation: {
      name: "New Delhi",
      lat: 28.6139,
      lon: 77.2090
    },
    preferences: {
      interests: ["commute", "fitness"],
      sensitivities: ["heat", "allergies"],
      commute_morning: "08:30",
      commute_evening: "18:00"
    },
    homeData: null,
    isOnline: navigator.onLine
  };

  // --- Weather Code SVG Icon Generator ---
  function getConditionSVG(iconName, isDay = true) {
    switch (iconName) {
      case 'sun':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <circle cx="32" cy="32" r="14" fill="#FBBF24" />
          <path d="M32 8v6M32 50v6M8 32h6M50 32h6M15 15l4.5 4.5M44.5 44.5L49 49M15 49l4.5-4.5M44.5 19.5L49 15" stroke="#F59E0B" stroke-width="3.5" stroke-linecap="round"/>
        </svg>`;
      case 'moon':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <path d="M42 46A20 20 0 1 1 42 18 16 16 0 0 0 42 46z" fill="#93C5FD" stroke="#60A5FA" stroke-width="2"/>
        </svg>`;
      case 'cloud-sun':
      case 'cloud-moon':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <circle cx="26" cy="24" r="11" fill="#FBBF24" />
          <path d="M22 46h24a12 12 0 0 0 2-23.8 15 15 0 0 0-28 6A11 11 0 0 0 22 46z" fill="#E2E8F0" />
        </svg>`;
      case 'cloud':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <path d="M18 46h28a13 13 0 0 0 2-25.8 17 17 0 0 0-32 7A12 12 0 0 0 18 46z" fill="#CBD5E1" />
        </svg>`;
      case 'cloud-rain':
      case 'cloud-drizzle':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <path d="M18 38h28a12 12 0 0 0 2-23.8 15 15 0 0 0-28 6A11 11 0 0 0 18 38z" fill="#94A3B8" />
          <line x1="22" y1="44" x2="19" y2="52" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
          <line x1="32" y1="44" x2="29" y2="52" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
          <line x1="42" y1="44" x2="39" y2="52" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
        </svg>`;
      case 'cloud-lightning':
      case 'cloud-lightning-rain':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <path d="M18 36h28a12 12 0 0 0 2-23.8 15 15 0 0 0-28 6A11 11 0 0 0 18 36z" fill="#64748B" />
          <polygon points="30 40 24 50 32 50 28 60 40 48 32 48" fill="#FBBF24" />
        </svg>`;
      case 'snowflake':
      case 'cloud-snow':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <circle cx="32" cy="32" r="10" fill="#BAE6FD"/>
          <line x1="32" y1="12" x2="32" y2="52" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
          <line x1="12" y1="32" x2="52" y2="32" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
        </svg>`;
      case 'cloud-fog':
        return `<svg viewBox="0 0 64 64" width="48" height="48">
          <line x1="16" y1="26" x2="48" y2="26" stroke="#CBD5E1" stroke-width="4" stroke-linecap="round"/>
          <line x1="12" y1="34" x2="52" y2="34" stroke="#CBD5E1" stroke-width="4" stroke-linecap="round"/>
          <line x1="20" y1="42" x2="44" y2="42" stroke="#CBD5E1" stroke-width="4" stroke-linecap="round"/>
        </svg>`;
      default:
        return `<svg viewBox="0 0 64 64" width="48" height="48"><circle cx="32" cy="32" r="14" fill="#FBBF24"/></svg>`;
    }
  }

  // --- Insight Category Emoji / Icon ---
  function getInsightEmoji(iconName) {
    const emojis = {
      umbrella: "☔",
      running: "🏃",
      leaf: "🌱",
      wind: "💨",
      sun: "☀️",
      snowflake: "❄️",
      "shield-alert": "🛡️",
      compass: "🧭",
      "cloud-rain": "🌧️"
    };
    return emojis[iconName] || "💡";
  }

  // --- Apply Localization ---
  function applyLanguage(lang) {
    state.language = lang;
    const t = TRANSLATIONS[lang] || TRANSLATIONS.en;

    // Translate all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (t[key]) {
        el.textContent = t[key];
      }
    });

    updateGreeting();
  }

  // --- Compute Greeting ---
  function updateGreeting() {
    const hour = new Date().getHours();
    const t = TRANSLATIONS[state.language] || TRANSLATIONS.en;
    let greeting = t.goodMorning;

    if (hour >= 12 && hour < 17) {
      greeting = t.goodAfternoon;
    } else if (hour >= 17 && hour < 21) {
      greeting = t.goodEvening;
    } else if (hour >= 21 || hour < 5) {
      greeting = t.goodNight;
    }

    const greetingEl = document.getElementById('greeting-text');
    if (greetingEl) greetingEl.textContent = greeting;
  }

  // --- Dynamic Hero Gradient Update ---
  function updateHeroGradient(weatherCode, isDay) {
    const hero = document.getElementById('hero-card');
    if (!hero) return;

    // Reset gradient classes
    hero.classList.remove('hero-clear-day', 'hero-clear-night', 'hero-cloudy', 'hero-rain', 'hero-thunderstorm');

    if (weatherCode in [95, 96, 99]) {
      hero.classList.add('hero-thunderstorm');
    } else if (weatherCode >= 51 && weatherCode <= 67 || weatherCode >= 80 && weatherCode <= 82) {
      hero.classList.add('hero-rain');
    } else if (weatherCode >= 2 && weatherCode <= 48) {
      hero.classList.add('hero-cloudy');
    } else if (!isDay) {
      hero.classList.add('hero-clear-night');
    } else {
      hero.classList.add('hero-clear-day');
    }
  }

  // --- Fetch Home API Data ---
  async function fetchHomeData() {
    const { lat, lon, name } = state.currentLocation;
    const url = `/api/home?user_id=${state.userId}&lat=${lat}&lon=${lon}&city_name=${encodeURIComponent(name)}`;

    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      state.homeData = data;
      renderHome(data);
    } catch (err) {
      console.warn('[Mausam] Fetch failed, checking cached state:', err);
      if (state.homeData) {
        renderHome(state.homeData);
      }
    }
  }

  // --- Render Entire Homepage ---
  function renderHome(data) {
    const curr = data.current;
    const metrics = data.metrics;
    const t = TRANSLATIONS[state.language] || TRANSLATIONS.en;

    // Update User Name
    if (data.user && data.user.name) {
      state.userName = data.user.name.split(' ')[0];
      document.getElementById('user-display-name').textContent = state.userName;
    }

    // 1. Header & Location
    document.getElementById('current-city-label').textContent = data.location_name;
    document.getElementById('hero-city-title').textContent = data.location_name;

    // Freshness chip
    const freshnessChip = document.getElementById('freshness-chip');
    const freshnessText = document.getElementById('freshness-text');
    if (freshnessText) {
      freshnessText.textContent = data.is_stale ? data.freshness_text : "Live data";
    }
    if (data.is_stale) {
      freshnessChip.classList.add('stale');
    } else {
      freshnessChip.classList.remove('stale');
    }

    // 2. Hero Card
    document.getElementById('hero-temp').textContent = `${Math.round(curr.temp)}°`;
    document.getElementById('hero-condition-text').textContent = curr.condition_text;
    document.getElementById('hero-feels-like').textContent = `Feels like ${Math.round(curr.feels_like)}°`;
    document.getElementById('hero-temp-high').textContent = `H: ${Math.round(curr.temp_max)}°`;
    document.getElementById('hero-temp-low').textContent = `L: ${Math.round(curr.temp_min)}°`;
    document.getElementById('hero-wind-summary').textContent = `Wind: ${curr.wind_speed} ${data.units === 'metric' ? 'km/h' : 'mph'} ${curr.wind_direction_cardinal}`;

    document.getElementById('hero-condition-icon').innerHTML = getConditionSVG(curr.condition_icon, curr.is_day);
    updateHeroGradient(curr.weather_code, curr.is_day);

    // 7. Severe Alerts
    renderAlerts(data.alerts || []);

    // 3. Personalized Smart Insights Strip
    renderTopInsights(data.insights_top || []);

    // 4. Hourly Forecast
    renderHourly(data.hourly || []);

    // 5. 7-Day Forecast
    renderDaily(data.daily || []);

    // 6. Key Metrics Grid
    renderMetrics(metrics, curr);

    // 8. Saved Cities Carousel
    renderSavedCities(data.saved_cities || []);

    // 9. Interest-Based Dynamic Card
    renderInterestCard(data.insights_all || [], data.active_interests || []);
  }

  // --- Render Alerts ---
  function renderAlerts(alerts) {
    const container = document.getElementById('alert-banner-container');
    const badge = document.getElementById('notif-badge');
    container.innerHTML = '';

    if (!alerts || alerts.length === 0) {
      badge.style.display = 'none';
      return;
    }

    badge.style.display = 'block';

    alerts.slice(0, 1).forEach((alert) => {
      const banner = document.createElement('div');
      banner.className = `alert-banner color-${alert.severity_color || 'yellow'}`;
      banner.id = `banner-${alert.id}`;
      banner.setAttribute('role', 'alert');

      banner.innerHTML = `
        <div class="alert-main">
          <div style="font-size: 1.3rem;">⚠️</div>
          <div>
            <div class="alert-title">${alert.title}</div>
            <div class="alert-desc">${alert.description}</div>
          </div>
        </div>
        <button class="alert-close-btn" aria-label="Dismiss alert" onclick="document.getElementById('banner-${alert.id}').classList.add('dismissed')">✕</button>
      `;
      container.appendChild(banner);
    });
  }

  // --- Render Top Insights ---
  function renderTopInsights(insights) {
    const list = document.getElementById('top-insights-list');
    list.innerHTML = '';

    if (!insights || insights.length === 0) {
      list.innerHTML = `<div class="insight-card"><p style="font-size:0.85rem; color:var(--text-muted);">Optimal weather conditions today. Enjoy your day!</p></div>`;
      return;
    }

    insights.forEach((ins) => {
      const card = document.createElement('div');
      card.className = `insight-card severity-${ins.severity}`;
      card.innerHTML = `
        <div class="insight-icon-box" aria-hidden="true">${getInsightEmoji(ins.icon)}</div>
        <div class="insight-content">
          <strong class="insight-title">${ins.title}</strong>
          <p class="insight-message">${ins.message}</p>
        </div>
      `;
      list.appendChild(card);
    });
  }

  // --- Render Hourly Forecast ---
  function renderHourly(hourly) {
    const rail = document.getElementById('hourly-scroll-rail');
    rail.innerHTML = '';

    hourly.forEach((item, idx) => {
      const card = document.createElement('div');
      card.className = `hourly-card ${idx === 0 ? 'active' : ''}`;
      card.setAttribute('role', 'listitem');

      card.innerHTML = `
        <span class="hourly-time">${item.hour_display}</span>
        <div class="hourly-icon" aria-hidden="true">${getConditionSVG(item.condition_icon, true)}</div>
        <strong class="hourly-temp">${Math.round(item.temp)}°</strong>
        <span class="hourly-rain" style="opacity: ${item.precipitation_prob > 0 ? 1 : 0};">💧 ${item.precipitation_prob}%</span>
      `;
      rail.appendChild(card);
    });
  }

  // --- Render 7-Day Forecast ---
  function renderDaily(daily) {
    const container = document.getElementById('daily-list-container');
    container.innerHTML = '';

    if (!daily || daily.length === 0) return;

    // Find overall range for temperature bars
    const allMins = daily.map(d => d.temp_min);
    const allMaxs = daily.map(d => d.temp_max);
    const minBound = Math.min(...allMins);
    const maxBound = Math.max(...allMaxs);
    const range = Math.max(1, maxBound - minBound);

    daily.forEach((day, idx) => {
      const row = document.createElement('div');
      row.className = 'daily-row';
      row.setAttribute('role', 'listitem');

      // Relative bar fill position
      const leftPercent = Math.max(0, ((day.temp_min - minBound) / range) * 100);
      const widthPercent = Math.max(15, ((day.temp_max - day.temp_min) / range) * 100);

      row.innerHTML = `
        <span class="daily-day">${idx === 0 ? 'Today' : day.day_display}</span>
        <div class="daily-icon" aria-hidden="true">${getConditionSVG(day.condition_icon, true)}</div>
        <div class="daily-bar-track" aria-hidden="true">
          <div class="daily-bar-fill" style="left: ${leftPercent}%; width: ${widthPercent}%;"></div>
        </div>
        <span class="daily-temp-min">${Math.round(day.temp_min)}°</span>
        <span class="daily-temp-max">${Math.round(day.temp_max)}°</span>
      `;
      container.appendChild(row);
    });
  }

  // --- Render Metrics Bento ---
  function renderMetrics(metrics, curr) {
    if (!metrics) return;

    document.getElementById('metric-humidity').textContent = `${metrics.humidity}%`;
    document.getElementById('metric-wind').textContent = `${metrics.wind_speed} ${state.units === 'metric' ? 'km/h' : 'mph'}`;
    document.getElementById('metric-wind-dir').textContent = `Direction: ${metrics.wind_direction_cardinal}`;

    document.getElementById('metric-uv').textContent = metrics.uv_index;
    const uvBadge = document.getElementById('metric-uv-badge');
    uvBadge.textContent = metrics.uv_level;
    uvBadge.style.background = metrics.uv_index >= 8 ? '#EF4444' : metrics.uv_index >= 5 ? '#F59E0B' : '#10B981';

    document.getElementById('metric-aqi').textContent = metrics.aqi;
    const aqiBadge = document.getElementById('metric-aqi-badge');
    aqiBadge.textContent = metrics.aqi_level;
    aqiBadge.style.background = metrics.aqi_color || '#F59E0B';

    document.getElementById('metric-visibility').textContent = `${metrics.visibility_km} km`;
    document.getElementById('metric-pressure').textContent = `${metrics.pressure_hpa} hPa`;
    document.getElementById('metric-sunrise').textContent = metrics.sunrise || '06:00';
    document.getElementById('metric-sunset').textContent = metrics.sunset || '18:30';
  }

  // --- Render Saved Cities ---
  function renderSavedCities(cities) {
    const rail = document.getElementById('saved-cities-rail');
    rail.innerHTML = '';

    cities.forEach((city) => {
      const card = document.createElement('div');
      const isCurrent = city.name.toLowerCase() === state.currentLocation.name.toLowerCase();
      card.className = `saved-city-card ${isCurrent ? 'active' : ''}`;
      card.setAttribute('role', 'listitem');
      card.tabIndex = 0;

      card.innerHTML = `
        <div class="city-card-header">
          <span class="city-card-name" title="${city.name}">${city.name}</span>
          <span style="font-size: 0.8rem;">${city.is_favorite ? '⭐' : ''}</span>
        </div>
        <div class="city-card-temp">${Math.round(city.temp)}°</div>
        <div class="city-card-condition">${city.condition_text}</div>
      `;

      card.addEventListener('click', () => {
        state.currentLocation = { name: city.name, lat: city.lat, lon: city.lon };
        fetchHomeData();
      });
      rail.appendChild(card);
    });

    // Add City Card Button
    const addCard = document.createElement('div');
    addCard.className = 'add-city-card';
    addCard.tabIndex = 0;
    addCard.setAttribute('role', 'button');
    addCard.setAttribute('aria-label', 'Add new city');
    addCard.innerHTML = `<span style="font-size: 1.5rem;">+</span><span>Add City</span>`;
    addCard.addEventListener('click', () => openCityModal());
    rail.appendChild(addCard);
  }

  // --- Render Interest-Based Card ---
  function renderInterestCard(allInsights, activeInterests) {
    const titleEl = document.getElementById('interest-title');
    const bodyEl = document.getElementById('interest-body');
    const badgeEl = document.getElementById('interest-badge');
    const iconEl = document.getElementById('interest-icon');

    // Pick top matching lifestyle insight
    const matched = allInsights.find(i => activeInterests.includes(i.category));
    if (matched) {
      titleEl.textContent = matched.title;
      bodyEl.textContent = matched.message;
      badgeEl.textContent = matched.category.toUpperCase();
      iconEl.textContent = getInsightEmoji(matched.icon);
    } else {
      titleEl.textContent = "Lifestyle Weather Guide";
      bodyEl.textContent = "Conditions are well-balanced for daily outdoor pursuits and smooth transit.";
      badgeEl.textContent = "OUTLOOK";
      iconEl.textContent = "✨";
    }
  }

  // --- Modal & Bottom Sheet Handlers ---
  const allInsightsModal = document.getElementById('all-insights-modal');
  const cityModal = document.getElementById('city-modal');
  const settingsModal = document.getElementById('settings-modal');

  function openAllInsights() {
    const list = document.getElementById('all-insights-full-list');
    list.innerHTML = '';
    const insights = (state.homeData && state.homeData.insights_all) || [];

    insights.forEach((ins) => {
      const card = document.createElement('div');
      card.className = `insight-card severity-${ins.severity}`;
      card.innerHTML = `
        <div class="insight-icon-box" aria-hidden="true">${getInsightEmoji(ins.icon)}</div>
        <div class="insight-content">
          <strong class="insight-title">${ins.title}</strong>
          <p class="insight-message">${ins.message}</p>
        </div>
      `;
      list.appendChild(card);
    });

    allInsightsModal.classList.add('open');
  }

  function closeAllInsights() {
    allInsightsModal.classList.remove('open');
  }

  function openCityModal() {
    cityModal.classList.add('open');
    const input = document.getElementById('city-search-input');
    input.value = '';
    document.getElementById('city-search-results').innerHTML = '';
    setTimeout(() => input.focus(), 150);
  }

  function closeCityModal() {
    cityModal.classList.remove('open');
  }

  function openSettingsModal() {
    settingsModal.classList.add('open');
  }

  function closeSettingsModal() {
    settingsModal.classList.remove('open');
  }

  // Close modals on backdrop click
  [allInsightsModal, cityModal, settingsModal].forEach((modal) => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('open');
      }
    });
  });

  document.getElementById('close-insights-modal').addEventListener('click', closeAllInsights);
  document.getElementById('close-city-modal').addEventListener('click', closeCityModal);
  document.getElementById('close-settings-modal').addEventListener('click', closeSettingsModal);
  document.getElementById('view-all-insights-btn').addEventListener('click', openAllInsights);
  document.getElementById('header-city-btn').addEventListener('click', openCityModal);
  document.getElementById('add-city-btn').addEventListener('click', openCityModal);

  // --- Geocoding Search Autocomplete ---
  let debounceTimeout = null;
  const searchInput = document.getElementById('city-search-input');
  searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimeout);
    const query = e.target.value.trim();
    if (query.length < 2) {
      document.getElementById('city-search-results').innerHTML = '';
      return;
    }

    debounceTimeout = setTimeout(async () => {
      try {
        const res = await fetch(`/api/geocode?q=${encodeURIComponent(query)}`);
        const results = await res.json();
        const resultsContainer = document.getElementById('city-search-results');
        resultsContainer.innerHTML = '';

        if (!results || results.length === 0) {
          resultsContainer.innerHTML = `<div style="padding:12px; font-size:0.85rem; color:var(--text-muted); text-align:center;">No cities found</div>`;
          return;
        }

        results.forEach((city) => {
          const item = document.createElement('div');
          item.className = 'search-result-item';
          item.innerHTML = `
            <div>
              <strong>${city.name}</strong>
              <div style="font-size:0.75rem; color:var(--text-muted);">${city.state ? city.state + ', ' : ''}${city.country}</div>
            </div>
            <button class="city-switcher-btn" style="padding: 4px 10px; font-size: 0.75rem;">Select</button>
          `;

          item.addEventListener('click', async () => {
            // Save city to user DB
            try {
              await fetch(`/api/users/${state.userId}/cities`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  name: city.name,
                  state: city.state,
                  country: city.country,
                  lat: city.lat,
                  lon: city.lon,
                  is_favorite: false
                })
              });
            } catch (err) {
              console.warn('Could not persist saved city:', err);
            }

            state.currentLocation = { name: city.name, lat: city.lat, lon: city.lon };
            closeCityModal();
            fetchHomeData();
          });

          resultsContainer.appendChild(item);
        });
      } catch (err) {
        console.warn('Geocoding error:', err);
      }
    }, 280);
  });

  // --- Settings & Preferences Management ---
  const btnUnitMetric = document.getElementById('btn-unit-metric');
  const btnUnitImperial = document.getElementById('btn-unit-imperial');
  const btnLangEn = document.getElementById('btn-lang-en');
  const btnLangHi = document.getElementById('btn-lang-hi');
  const btnLangTa = document.getElementById('btn-lang-ta');

  btnUnitMetric.addEventListener('click', () => {
    state.units = 'metric';
    btnUnitMetric.classList.add('active');
    btnUnitImperial.classList.remove('active');
  });

  btnUnitImperial.addEventListener('click', () => {
    state.units = 'imperial';
    btnUnitImperial.classList.add('active');
    btnUnitMetric.classList.remove('active');
  });

  [btnLangEn, btnLangHi, btnLangTa].forEach((btn) => {
    btn.addEventListener('click', () => {
      [btnLangEn, btnLangHi, btnLangTa].forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const lang = btn.id.split('-').pop();
      applyLanguage(lang);
    });
  });

  // Chip toggles for Interests & Sensitivities
  document.querySelectorAll('#interests-selector .chip-item').forEach((chip) => {
    chip.addEventListener('click', () => chip.classList.toggle('active'));
  });

  document.querySelectorAll('#sensitivities-selector .chip-item').forEach((chip) => {
    chip.addEventListener('click', () => chip.classList.toggle('active'));
  });

  document.getElementById('save-preferences-btn').addEventListener('click', async () => {
    const selectedInterests = Array.from(document.querySelectorAll('#interests-selector .chip-item.active'))
      .map(c => c.getAttribute('data-val'));
    const selectedSensitivities = Array.from(document.querySelectorAll('#sensitivities-selector .chip-item.active'))
      .map(c => c.getAttribute('data-val'));
    const morning = document.getElementById('time-morning').value || "08:30";
    const evening = document.getElementById('time-evening').value || "18:00";

    const payload = {
      units: state.units,
      language: state.language,
      interests: selectedInterests,
      sensitivities: selectedSensitivities,
      commute_morning: morning,
      commute_evening: evening
    };

    try {
      await fetch(`/api/users/${state.userId}/preferences`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } catch (err) {
      console.warn('Preferences update failed:', err);
    }

    closeSettingsModal();
    fetchHomeData();
  });

  // --- Bottom Navigation Routing ---
  document.querySelectorAll('.nav-item').forEach((item) => {
    item.addEventListener('click', (e) => {
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');

      const target = item.getAttribute('data-nav');
      if (target === 'home') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else if (target === 'forecast') {
        document.getElementById('hourly-section').scrollIntoView({ behavior: 'smooth' });
      } else if (target === 'cities') {
        document.getElementById('saved-cities-section').scrollIntoView({ behavior: 'smooth' });
      } else if (target === 'profile') {
        openSettingsModal();
      } else if (target === 'map') {
        // Open map radar placeholder / alert
        alert("Radar Map: High-definition precipitation radar tiles are scheduled for next release.");
      }
    });
  });

  // --- Offline & Network Listener ---
  const offlineBanner = document.getElementById('offline-banner');
  function handleNetworkChange() {
    if (navigator.onLine) {
      offlineBanner.classList.add('hidden');
      fetchHomeData();
    } else {
      offlineBanner.classList.remove('hidden');
    }
  }

  window.addEventListener('online', handleNetworkChange);
  window.addEventListener('offline', handleNetworkChange);
  document.getElementById('retry-offline-btn').addEventListener('click', () => {
    handleNetworkChange();
  });

  // --- Initial Bootstrap ---
  updateGreeting();
  fetchHomeData();

})();
