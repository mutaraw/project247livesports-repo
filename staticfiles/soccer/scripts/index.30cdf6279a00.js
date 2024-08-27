let groupedFixtures = {};  // Will be populated by WebSocket data
const socketProtocol = (window.location.protocol === 'https:') ? 'wss://' : 'ws://';
const socket = new WebSocket(socketProtocol + window.location.host + '/ws/fixtures/');

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    groupedFixtures = data.fixtures;  // Update global variable
    updateUI();
};

document.addEventListener('DOMContentLoaded', function () {
    const lastTab = localStorage.getItem('selectedTab') || 'live';
    showTab(lastTab);
});

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(section => {
        section.style.display = 'none';
    });
    document.querySelector(`#${tabId}`).style.display = 'block';

    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(`tab-${tabId}`).classList.add('active');

    localStorage.setItem('selectedTab', tabId);
}

function updateUI() {
    const favorites = getFavorites();

    document.querySelector('#live').innerHTML = renderFixtures(groupedFixtures.live);
    document.querySelector('#scheduled').innerHTML = renderFixtures(groupedFixtures.scheduled);
    document.querySelector('#finished').innerHTML = renderFixtures(groupedFixtures.finished);
    document.querySelector('#notplayed').innerHTML = renderFixtures(groupedFixtures.notplayed);

    document.querySelector('#favorites-container').innerHTML = renderFavorites(favorites, groupedFixtures);
    updateFavoriteIcons(favorites);  // Update icons after rendering
}

function getFavorites() {
    return (JSON.parse(localStorage.getItem('favorites')) || []).filter(id => id !== null);
}

function saveFavorites(favorites) {
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

function toggleFavorite(fixtureId) {
    let favorites = getFavorites();
    if (favorites.includes(fixtureId)) {
        favorites = favorites.filter(id => id !== fixtureId);
    } else {
        favorites.push(fixtureId);
    }
    saveFavorites(favorites);
    updateUI();  // Re-render the fixtures to reflect changes
}

function updateFavoriteIcons(favorites) {
    document.querySelectorAll('.fixture').forEach(fixture => {
        const fixtureId = parseInt(fixture.getAttribute('data-id'));
        const starIcon = fixture.querySelector('.fa-star');
        if (favorites.includes(fixtureId)) {
            starIcon.classList.add('favorite');
        } else {
            starIcon.classList.remove('favorite');
        }
        starIcon.onclick = () => toggleFavorite(fixtureId);
    });
}

function renderFixtures(fixtures) {
    let html = '';
    for (let league in fixtures) {
        for (let date in fixtures[league]) {
            if (fixtures[league][date] && fixtures[league][date].length > 0) {
                const utcDate = new Date(date + ' UTC');
                const localDate = convertToLocalTime(utcDate);
                const formattedDate = formatLocalDate(localDate);

                html += `<div class="card">
                    <div class="card-head">
                        <div class="card-head-left">
                            ${fixtures[league][date][0].league_country_flag ?
                    `<img src="${fixtures[league][date][0].league_country_flag}" alt="${fixtures[league][date][0].league_country}" loading="lazy"/>` : ''}
                            ${fixtures[league][date][0].league_logo ?
                    `<img src="${fixtures[league][date][0].league_logo}" alt="${fixtures[league][date][0].league_name}" loading="lazy"/>` : ''}
                            ${fixtures[league][date][0].league_country && fixtures[league][date][0].league_name ?
                    `<div>${fixtures[league][date][0].league_country} : ${fixtures[league][date][0].league_name}</div>` : ''}
                        </div>
                        <div class="card-head-right">
                            <div class="card-date">${formattedDate}</div>
                        </div>
                    </div>
                    <div class="card-body">`;

                fixtures[league][date].forEach(fixture => {
                    const isFavorite = getFavorites().includes(fixture.fixture_id);
                    html += `<div class="fixture" data-id="${fixture.fixture_id}">
                        <div class="home-team">
                            ${fixture.home_team_logo ?
                        `<img src="${fixture.home_team_logo}" alt="${fixture.home_team_name}" loading="lazy">` : ''}
                            ${fixture.home_team_name ?
                        `<div class="home-team-name">${fixture.home_team_name}</div>` : ''}
                        </div>
                        <div class="home-goals">
                            ${fixture.home_goals !== null ? `<div>${fixture.home_goals}</div>` : ''}
                        </div>
                        <div class="away-goals">
                            ${fixture.away_goals !== null ? `<div>${fixture.away_goals}</div>` : ''}
                        </div>
                        <div class="home-team-winner">
                            ${fixture.home_team_winner === true ?
                        `<i class="fa-solid fa-arrow-up"></i>` :
                        fixture.home_team_winner === false ?
                            `<i class="fa-solid fa-arrow-down"></i>` :
                            `<i class="fa-solid fa-arrows-up-down"></i>`}
                        </div>
                        <div class="away-team-winner">
                            ${fixture.away_team_winner === true ?
                        `<i class="fa-solid fa-arrow-up"></i>` :
                        fixture.away_team_winner === false ?
                            `<i class="fa-solid fa-arrow-down"></i>` :
                            `<i class="fa-solid fa-arrows-up-down"></i>`}
                        </div>
                        <div class="away-team">
                            ${fixture.away_team_logo ?
                        `<img src="${fixture.away_team_logo}" alt="${fixture.away_team_name}" loading="lazy">` : ''}
                            ${fixture.away_team_name ?
                        `<div class="away-team-name">${fixture.away_team_name}</div>` : ''}
                        </div>
                        <div class="statuses">
                            <div class="status-short">
                                ${fixture.status_short ? `<div>${fixture.status_short}</div>` : ''}
                            </div>
                            <div class="status-elapsed">
                                ${fixture.status_elapsed ? `<div>${fixture.status_elapsed}<span>'</span></div>` : ''}
                            </div>
                        </div>
                        <div class="match-fav">
                            <i class="fa-solid fa-star ${isFavorite ? 'favorite' : ''}" onclick="toggleFavorite(${fixture.fixture_id})"></i>
                        </div>
                        <div class="match-goals">
                            ${fixture.halftime_home !== null ? `<div class="ht">HT: ${fixture.halftime_home} - ${fixture.halftime_away}</div>` : ''}
                            ${fixture.fulltime_home !== null ? `<div class="ft">FT: ${fixture.fulltime_home} - ${fixture.fulltime_away}</div>` : ''}
                            ${fixture.extratime_home !== null ? `<div class="et">${fixture.extratime_home} - ${fixture.extratime_away}</div>` : ''}
                            ${fixture.penalty_home !== null ? `<div class="pen">${fixture.penalty_home} - ${fixture.penalty_away}</div>` : ''}
                        </div>
                    </div>`;
                });

                html += `</div></div>`;
            }
        }
    }
    return html;
}

function renderFavorites(favorites, groupedFixtures) {
    let html = '<div style="padding: 10px; background: tomato; border-radius: 5px; color: #ffffff; font-size: 16px; font-weight:bold;"><i class="fa-solid fa-star" style="font-weight: bold; font-size: 18px;"></i> Favorite Live Matches</div>';
    let foundFavorites = false;

    for (let league in groupedFixtures.live) {
        for (let date in groupedFixtures.live[league]) {
            groupedFixtures.live[league][date].forEach(fixture => {
                if (favorites.includes(fixture.fixture_id)) {
                    foundFavorites = true;
                    html += `<div class="card">
                        <div class="fixture" data-id="${fixture.fixture_id}">
                            <div class="home-team">
                                ${fixture.home_team_logo ?
                        `<img src="${fixture.home_team_logo}" alt="${fixture.home_team_name}" loading="lazy">` : ''}
                                ${fixture.home_team_name ?
                        `<div class="home-team-name">${fixture.home_team_name}</div>` : ''}
                            </div>
                            <div class="home-goals">
                                ${fixture.home_goals !== null ? `<div>${fixture.home_goals}</div>` : ''}
                            </div>
                            <div class="away-goals">
                                ${fixture.away_goals !== null ? `<div>${fixture.away_goals}</div>` : ''}
                            </div>
                            <div class="home-team-winner">
                                ${fixture.home_team_winner === true ?
                        `<i class="fa-solid fa-arrow-up"></i>` :
                        fixture.home_team_winner === false ?
                            `<i class="fa-solid fa-arrow-down"></i>` :
                            `<i class="fa-solid fa-arrows-up-down"></i>`}
                            </div>
                            <div class="away-team-winner">
                                ${fixture.away_team_winner === true ?
                        `<i class="fa-solid fa-arrow-up"></i>` :
                        fixture.away_team_winner === false ?
                            `<i class="fa-solid fa-arrow-down"></i>` :
                            `<i class="fa-solid fa-arrows-up-down"></i>`}
                            </div>
                            <div class="away-team">
                                ${fixture.away_team_logo ?
                        `<img src="${fixture.away_team_logo}" alt="${fixture.away_team_name}" loading="lazy">` : ''}
                                ${fixture.away_team_name ?
                        `<div class="away-team-name">${fixture.away_team_name}</div>` : ''}
                            </div>
                            <div class="statuses">
                                <div class="status-short">
                                    ${fixture.status_short ? `<div>${fixture.status_short}</div>` : ''}
                                </div>
                                <div class="status-elapsed">
                                    ${fixture.status_elapsed ? `<div>${fixture.status_elapsed}<span>'</span></div>` : ''}
                                </div>
                            </div>
                            <div class="match-fav">
                                <i class="fa-solid fa-star favorite" onclick="toggleFavorite(${fixture.fixture_id})"></i>
                            </div>
                            <div class="match-goals">
                                ${fixture.halftime_home !== null ? `<div class="ht">HT: ${fixture.halftime_home} - ${fixture.halftime_away}</div>` : ''}
                                ${fixture.fulltime_home !== null ? `<div class="ft">FT: ${fixture.fulltime_home} - ${fixture.fulltime_away}</div>` : ''}
                                ${fixture.extratime_home !== null ? `<div class="et">${fixture.extratime_home} - ${fixture.extratime_away}</div>` : ''}
                                ${fixture.penalty_home !== null ? `<div class="pen">${fixture.penalty_home} - ${fixture.penalty_away}</div>` : ''}
                            </div>
                        </div>
                    </div>`;
                }
            });
        }
    }

    if (!foundFavorites) {
        html += '<p style="text-align: center;">No favorite matches yet. Click the star icon to see them appear here.</p>';
    }

    return html;
}

function convertToLocalTime(date) {
    return new Date(date.toLocaleString('en-US', {timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone}));
}

function formatLocalDate(date) {
    const options = {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
    };
    return date.toLocaleString('en-US', options).replace(',', ' @');
}
