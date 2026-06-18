// ========== 全域共用 JavaScript ==========
// 主題系統
const GLOBAL_THEMES = [
    'theme-pina-colada', 'theme-dark-stormy', 'theme-glass-window', 'theme-forest-bath',
    'theme-mint-garden', 'theme-apple-cider', 'theme-nightcap', 'theme-sunrise'
];

function setThemeByIndex(index) {
    GLOBAL_THEMES.forEach(t => document.body.classList.remove(t));
    document.body.classList.add(GLOBAL_THEMES[index]);
    const slider = document.getElementById('themeSlider');
    if (slider) slider.value = index;
    localStorage.setItem('selected_theme_index', index);
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function initTheme(defaultIndex = 3) {
    const saved = localStorage.getItem('selected_theme_index');
    setThemeByIndex(saved !== null ? parseInt(saved) : defaultIndex);
}

// 字體系統 + 頁尾 padding 動態調整
let globalResizeObserver = null;

function updateBodyPaddingForFooter() {
    const footer = document.getElementById('footer');
    const bottomNav = document.getElementById('bottomNavBar');
    if (!footer || !bottomNav) return;
    const totalPadding = footer.offsetHeight + bottomNav.offsetHeight + 30;
    document.body.style.paddingBottom = totalPadding + 'px';
}

function setFontSize(size) {
    const html = document.documentElement;
    html.classList.remove('font-small', 'font-standard', 'font-xlarge');
    if (size === 'small') html.classList.add('font-small');
    else if (size === 'xlarge') html.classList.add('font-xlarge');
    else html.classList.add('font-standard');
    localStorage.setItem('elderly_font', size);
    document.querySelectorAll('.font-switch-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-font') === size) btn.classList.add('active');
    });
    if (typeof lucide !== 'undefined') lucide.createIcons();
    setTimeout(() => updateBodyPaddingForFooter(), 100);
}

function initFont(defaultSize = 'standard') {
    const saved = localStorage.getItem('elderly_font');
    const size = (saved === 'small' || saved === 'xlarge') ? saved : defaultSize;
    setFontSize(size);
}

// 滾動控制頂部/底部導航
let globalTicking = false;
const globalTopNavBar = document.getElementById('topNavBar');
const globalBottomNavBar = document.getElementById('bottomNavBar');
const globalMacTopbar = document.querySelector('.mac-topbar');

function adjustTopNavPosition() {
    if (globalMacTopbar && globalTopNavBar) {
        globalTopNavBar.style.top = globalMacTopbar.offsetHeight + 'px';
    }
}

function handleScroll() {
    const currentScrollY = window.scrollY;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const isNearBottom = currentScrollY + windowHeight >= documentHeight - 150;
    if (isNearBottom) {
        if (globalTopNavBar) globalTopNavBar.classList.add('hide');
        if (globalBottomNavBar) globalBottomNavBar.classList.remove('hide');
    } else {
        if (globalTopNavBar) globalTopNavBar.classList.remove('hide');
        if (globalBottomNavBar) globalBottomNavBar.classList.add('hide');
    }
    globalTicking = false;
}

function initScrollHandler() {
    window.addEventListener('scroll', () => {
        if (!globalTicking) {
            requestAnimationFrame(handleScroll);
            globalTicking = true;
        }
    });
    if (globalBottomNavBar) globalBottomNavBar.classList.add('hide');
}

// 導航綁定（頂部/底部）
function bindGlobalNavigation() {
    document.querySelectorAll('.top-nav-item, .bottom-nav-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const page = btn.getAttribute('data-page');
            if (page === 'index') window.location.href = 'index.html';
            else if (page) window.location.href = page + '.html';
        });
    });
}

// 控制中心邏輯
let globalToolsHidden = false;
const globalFontGroup = document.querySelector('.font-switch-group');
const globalThemeWidget = document.querySelector('.theme-slider-widget');
const globalHideToolsBtn = document.getElementById('hideToolsBtn');

function toggleToolsVisibility() {
    globalToolsHidden = !globalToolsHidden;
    if (globalFontGroup) globalFontGroup.style.display = globalToolsHidden ? 'none' : 'inline-flex';
    if (globalThemeWidget) globalThemeWidget.style.display = globalToolsHidden ? 'none' : 'inline-flex';
    if (globalHideToolsBtn) globalHideToolsBtn.textContent = globalToolsHidden ? '🔧 顯示字體與主題工具' : '🔧 隱藏字體與主題工具';
    localStorage.setItem('tools_hidden', globalToolsHidden);
}

function initToolsVisibility() {
    const saved = localStorage.getItem('tools_hidden');
    if (saved === 'true') {
        globalToolsHidden = true;
        if (globalFontGroup) globalFontGroup.style.display = 'none';
        if (globalThemeWidget) globalThemeWidget.style.display = 'none';
        if (globalHideToolsBtn) globalHideToolsBtn.textContent = '🔧 顯示字體與主題工具';
    } else {
        globalToolsHidden = false;
        if (globalFontGroup) globalFontGroup.style.display = 'inline-flex';
        if (globalThemeWidget) globalThemeWidget.style.display = 'inline-flex';
        if (globalHideToolsBtn) globalHideToolsBtn.textContent = '🔧 隱藏字體與主題工具';
    }
}

function initControlCenter() {
    let panelVisible = false;
    const panel = document.getElementById('controlCenterPanel');
    const controlBtn = document.getElementById('controlCenterBtn');
    if (controlBtn) {
        controlBtn.addEventListener('click', () => {
            panelVisible = !panelVisible;
            if (panel) panel.style.display = panelVisible ? 'block' : 'none';
            if (panelVisible && typeof lucide !== 'undefined') lucide.createIcons();
        });
    }
    const closePanel = document.getElementById('closeControlPanel');
    if (closePanel) closePanel.addEventListener('click', () => { if (panel) panel.style.display = 'none'; panelVisible = false; });
    if (globalHideToolsBtn) globalHideToolsBtn.addEventListener('click', toggleToolsVisibility);
    
    document.querySelectorAll('.theme-option-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            setThemeByIndex(parseInt(btn.getAttribute('data-theme-index')));
            if (panel) panel.style.display = 'none';
            panelVisible = false;
        });
    });
    document.querySelectorAll('.font-switch-btn').forEach(btn => {
        btn.addEventListener('click', () => setFontSize(btn.getAttribute('data-font')));
    });
    const themeSlider = document.getElementById('themeSlider');
    if (themeSlider) themeSlider.addEventListener('input', (e) => setThemeByIndex(parseInt(e.target.value)));
}

// 其他公共按鈕：求助 FAB、隱私權、主頁 Logo、登入按鈕（登入狀態模擬）
function updateLoginButton() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const loginBtn = document.getElementById('loginBtn');
    const loginBtnText = document.getElementById('loginBtnText');
    if (!loginBtn || !loginBtnText) return;
    if (isLoggedIn) {
        loginBtnText.innerText = '我的帳戶';
        const icon = loginBtn.querySelector('i[data-lucide]');
        if (icon) icon.setAttribute('data-lucide', 'user');
    } else {
        loginBtnText.innerText = '登入';
        const icon = loginBtn.querySelector('i[data-lucide]');
        if (icon) icon.setAttribute('data-lucide', 'log-in');
    }
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function handleLoginClick(e) {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (isLoggedIn) window.location.href = 'dashboard.html';
    else window.location.href = 'login.html';
}

function bindGlobalButtons() {
    const helpFab = document.getElementById('helpFabBtn');
    if (helpFab) helpFab.addEventListener('click', () => window.location.href = 'helps.html');
    const privacyBtn = document.getElementById('privacyBtn');
    if (privacyBtn) privacyBtn.addEventListener('click', () => alert('隱私權政策：我們嚴格保護您的個人資料，不會與第三方分享。'));
    const homeLogo = document.getElementById('homeLogoBtn');
    if (homeLogo) homeLogo.addEventListener('click', () => window.location.href = 'index.html');
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) loginBtn.addEventListener('click', handleLoginClick);
    updateLoginButton();
}

// 響應式調整
let globalResizeTimeout;
window.addEventListener('resize', () => {
    if (globalResizeTimeout) clearTimeout(globalResizeTimeout);
    globalResizeTimeout = setTimeout(() => {
        adjustTopNavPosition();
        updateBodyPaddingForFooter();
    }, 150);
});

// 初始化全域 UI（需傳入頁面專屬默認主題索引和字體大小）
function initGlobalUI(options = {}) {
    const defaultTheme = options.defaultThemeIndex !== undefined ? options.defaultThemeIndex : 3;
    const defaultFont = options.defaultFontSize || 'standard';
    initTheme(defaultTheme);
    initFont(defaultFont);
    initToolsVisibility();
    adjustTopNavPosition();
    initScrollHandler();
    bindGlobalNavigation();
    bindGlobalButtons();
    initControlCenter();
    updateBodyPaddingForFooter();
    if (typeof lucide !== 'undefined') lucide.createIcons();
}