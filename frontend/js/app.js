/**
 * LPU ExamPrep AI — App Controller
 */

class LPUExamPrepApp {
  constructor() {
    this.currentUser = null;
    this.activePage = 'home';
    this.activeSubject = 'CSE305';
    this.currentMockQuestions = [];
    this.testStartTime = null;
    this.init();
  }

  async init() {
    this.checkLoginState();
    await this.loadSubjects();
    this.loadAnalytics();
  }

  checkLoginState() {
    const userStr = localStorage.getItem('lpu_user');
    if (userStr) {
      this.currentUser = JSON.parse(userStr);
      this.updateUserHeader();
    } else {
      this.autoLoginDemo('aarav@lpu.in', 'password123');
    }
  }

  async autoLoginDemo(email, pwd) {
    try {
      const res = await ApiService.login(email, pwd);
      this.currentUser = res.user_profile;
      this.updateUserHeader();
      this.renderLiveStatsBanner();
    } catch (e) {
      console.warn('Auto login failed:', e);
    }
  }

  async quickLogin(email, pwd, regNumber = '') {
    const errDiv = document.getElementById('login-error-msg');
    if (errDiv) errDiv.innerText = '';
    try {
      const res = await ApiService.login(email, pwd, regNumber);
      this.currentUser = res.user_profile;
      this.updateUserHeader();
      this.renderLiveStatsBanner();
      this.switchPage('dashboard');
    } catch (e) {
      if (errDiv) errDiv.innerText = 'Sign In Failed: ' + e.message;
    }
  }

  async handleLoginSubmit(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const pwd = document.getElementById('login-password').value;
    const regNumber = document.getElementById('login-reg-number')?.value || '';

    if (!regNumber || !regNumber.trim()) {
      const errDiv = document.getElementById('login-error-msg');
      if (errDiv) errDiv.innerText = 'LPU Registration Number is strictly mandatory.';
      return;
    }

    await this.quickLogin(email, pwd, regNumber);
  }

  async handleRegisterSubmit(e) {
    e.preventDefault();
    const fullName = document.getElementById('reg-fullname').value;
    const regNumber = document.getElementById('reg-number').value;
    const email = document.getElementById('reg-email').value;
    const programId = document.getElementById('reg-program').value;
    const password = document.getElementById('reg-password').value;
    const errDiv = document.getElementById('register-error-msg');

    if (errDiv) errDiv.innerText = '';

    if (!regNumber || !regNumber.trim()) {
      if (errDiv) errDiv.innerText = 'LPU Registration Number is strictly mandatory.';
      return;
    }

    try {
      const res = await ApiService.register(fullName, email, password, regNumber, programId);
      this.currentUser = res.user_profile;
      this.updateUserHeader();
      this.renderLiveStatsBanner();
      alert(`Registration Successful! Welcome to LPU ExamPrep AI, ${fullName}.`);
      this.switchPage('dashboard');
    } catch (err) {
      if (errDiv) errDiv.innerText = 'Registration Error: ' + err.message;
    }
  }

  async handleOAuthLogin(provider) {
    const regNumber = prompt(`Please enter your mandatory LPU Registration Number to continue with ${provider}:`, '12204891');
    if (!regNumber || !regNumber.trim()) {
      alert('Authentication cancelled: LPU Registration Number is strictly mandatory.');
      return;
    }

    try {
      const dummyEmail = `student_${provider.toLowerCase()}@lpu.in`;
      const dummyName = `${provider} LPU Student`;
      const res = await ApiService.oauthLogin(provider.toLowerCase(), dummyEmail, dummyName, regNumber.trim());
      this.currentUser = res.user_profile;
      this.updateUserHeader();
      this.renderLiveStatsBanner();
      alert(`Authenticated successfully via ${provider}!`);
      this.switchPage('dashboard');
    } catch (e) {
      alert(`${provider} Auth Error: ` + e.message);
    }
  }

  updateUserHeader() {
    const header = document.getElementById('user-header');
    if (!header) return;

    if (this.currentUser) {
      header.innerHTML = `
        <span class="badge badge-purple">${this.currentUser.role}</span>
        <span style="font-size: 0.9rem; font-weight: 600; color: #fff;">${this.currentUser.full_name} (${this.currentUser.email})</span>
        <button class="btn btn-secondary" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;" onclick="app.logout()">Logout</button>
      `;
    } else {
      header.innerHTML = `
        <button class="btn" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;" onclick="app.switchPage('login')">🔑 Student Login</button>
      `;
    }
  }

  renderLiveStatsBanner() {
    const banner = document.getElementById('live-user-stats-bar');
    if (!banner) return;

    if (!this.currentUser) {
      banner.style.display = 'none';
      return;
    }

    const reg = this.currentUser.registration_number || '12204891';
    const mockCount = this.mockTestHistory ? this.mockTestHistory.length : 1;
    const avgScore = 86;

    banner.style.display = 'block';
    banner.innerHTML = `
      <div class="glass-panel" style="padding: 1rem 1.25rem; background: linear-gradient(135deg, rgba(126, 34, 206, 0.25), rgba(30, 58, 138, 0.2)); border: 1px solid rgba(192, 132, 252, 0.3); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="width: 42px; height: 42px; border-radius: 50%; background: var(--lpu-purple); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; color: #fff; box-shadow: 0 0 12px rgba(126, 34, 206, 0.5);">
            ${this.currentUser.full_name.charAt(0)}
          </div>
          <div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #fff;">
              ${this.currentUser.full_name} <span style="font-size: 0.78rem; color: var(--text-muted); font-weight: 400;">(Reg #${reg})</span>
            </div>
            <div style="font-size: 0.78rem; color: #c084fc;">
              B.Tech CSE • Year 2 • Semester 3 Active
            </div>
          </div>
        </div>

        <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center;">
          <div style="text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #38bdf8;">9</div>
            <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Sem 3 Subjects</div>
          </div>
          <div style="text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #34d399;">${mockCount}</div>
            <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">AI Tests Taken</div>
          </div>
          <div style="text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #f43f5e;">${avgScore}%</div>
            <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Avg Accuracy</div>
          </div>
          <div style="text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #c084fc;">88/100</div>
            <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">AI Readiness Index</div>
          </div>
        </div>
      </div>
    `;
  }

  logout() {
    ApiService.clearAuthToken();
    location.reload();
  }

  switchPage(pageId) {
    this.activePage = pageId;
    document.querySelectorAll('.page-section').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn, .mobile-nav-item').forEach(el => el.classList.remove('active'));

    const targetView = document.getElementById(`page-${pageId}`);
    if (targetView) targetView.classList.add('active');

    const targetTab = document.getElementById(`tab-${pageId}`);
    if (targetTab) targetTab.classList.add('active');

    const targetMobile = document.getElementById(`mnav-${pageId}`);
    if (targetMobile) targetMobile.classList.add('active');

    if (pageId === 'subjects') this.loadSubjects();
    if (pageId === 'domains') this.loadSubjectDomains();
    if (pageId === 'electives') this.loadElectivesHub();
    if (pageId === 'pedagogy') this.loadPedagogyAndPartners();
    if (pageId === 'analyzer') this.openAIAnalyzer(this.activeSubject);
    if (pageId === 'dashboard') this.loadAnalytics();
  }

  async loadSubjectDomains() {
    const container = document.getElementById('domains-grid');
    if (!container) return;

    try {
      const domains = await ApiService.getSubjectDomains();
      let html = domains.map(d => `
        <div class="glass-panel card-item">
          <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
            <span style="font-size: 1.6rem;">${d.icon}</span>
            <h3 style="font-size: 1.1rem; color: #c084fc;">${d.title}</h3>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.4;">${d.description}</p>
          <div style="margin-top: 0.75rem;">
            <strong style="font-size: 0.8rem; color: var(--lpu-cyan); display: block; margin-bottom: 0.3rem;">Core Subjects Covered:</strong>
            <ul style="padding-left: 1.2rem; font-size: 0.82rem; color: var(--text-primary); line-height: 1.6;">
              ${d.subjects.map(s => `<li>${s}</li>`).join('')}
            </ul>
          </div>
        </div>
      `).join('');
      container.innerHTML = html;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }

  async loadElectivesHub() {
    const container = document.getElementById('electives-grid');
    if (!container) return;

    try {
      const categories = await ApiService.getElectiveCategories();
      let html = categories.map(c => `
        <div class="glass-panel card-item">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <h3 style="font-size: 1.1rem; color: var(--text-primary);">${c.category}</h3>
            <span class="badge badge-purple">${c.badge}</span>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.4;">${c.description}</p>
          <div style="margin-top: 0.75rem;">
            <strong style="font-size: 0.8rem; color: var(--accent-emerald); display: block; margin-bottom: 0.3rem;">Available Courses / Options:</strong>
            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.4rem;">
              ${c.options.map(opt => `<span style="font-size: 0.78rem; background: rgba(255,255,255,0.04); padding: 0.3rem 0.6rem; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">${opt}</span>`).join('')}
            </div>
          </div>
        </div>
      `).join('');
      container.innerHTML = html;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }

  async loadPedagogyAndPartners() {
    const pillarsContainer = document.getElementById('pedagogy-pillars-container');
    const partnersContainer = document.getElementById('partners-cloud-container');
    if (!pillarsContainer || !partnersContainer) return;

    try {
      const data = await ApiService.getPedagogyAndPartners();
      
      let pthml = data.pedagogy_pillars.map((p, idx) => `
        <div class="glass-panel card-item">
          <div style="display: flex; align-items: center; gap: 0.6rem;">
            <span class="badge badge-blue">Pillar #${idx + 1}</span>
            <h4 style="color: #60a5fa;">${p.title}</h4>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.4;">${p.desc}</p>
        </div>
      `).join('');
      pillarsContainer.innerHTML = pthml;

      let prthml = data.industry_partners.map(part => `
        <span style="background: rgba(126, 34, 206, 0.15); border: 1px solid rgba(192, 132, 252, 0.3); color: #c084fc; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 700; font-size: 0.88rem; display: inline-flex; align-items: center; gap: 0.4rem;">
          🤝 ${part}
        </span>
      `).join('');
      partnersContainer.innerHTML = prthml;

    } catch (e) {
      pillarsContainer.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }

  async openProgramYearsView(programId = 1, programName = 'B.Tech CSE') {
    this.selectedProgramName = programName;
    this.switchPage('subjects');
    this.renderYearNavigationCards();
  }

  renderYearNavigationCards(selectedYear = null, activeSem = null) {
    const navContainer = document.getElementById('year-navigator-container');
    if (!navContainer) return;

    const progName = this.selectedProgramName || 'B.Tech CSE';
    
    let semPillHtml = '';
    if (selectedYear) {
      const s1 = (selectedYear - 1) * 2 + 1;
      const s2 = s1 + 1;
      semPillHtml = `
        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
          <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Select Semester:</span>
          <button class="btn ${activeSem === s1 ? '' : 'btn-secondary'}" style="font-size: 0.78rem; padding: 0.3rem 0.8rem;" onclick="app.selectSemester(${s1}, ${selectedYear})">
            🍂 Semester ${s1} (Autumn Term)
          </button>
          <button class="btn ${activeSem === s2 ? '' : 'btn-secondary'}" style="font-size: 0.78rem; padding: 0.3rem 0.8rem;" onclick="app.selectSemester(${s2}, ${selectedYear})">
            🌸 Semester ${s2} (Spring Term)
          </button>
        </div>
      `;
    }

    let html = `
      <div class="glass-panel" style="padding: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
          <div style="font-size: 0.9rem; font-weight: 700; color: #c084fc;">
            🎓 Academic Program: <strong>${progName}</strong> ${selectedYear ? `➜ Year ${selectedYear}` : ''} ${activeSem ? `➜ Semester ${activeSem}` : ''}
          </div>
          <button class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem;" onclick="app.renderYearNavigationCards(null); app.loadSubjects();">All 4 Years</button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div class="glass-panel" style="padding: 1rem; cursor: pointer; border-color: ${selectedYear === 1 ? 'var(--lpu-purple)' : 'var(--panel-border)'};" onclick="app.selectYear(1)">
            <div style="font-size: 0.8rem; color: #c084fc; font-weight: 700;">YEAR 1 (Freshman)</div>
            <div style="font-size: 1rem; font-weight: 700; margin-top: 0.2rem;">1st Year</div>
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.4rem;">Semesters 1 & 2</div>
          </div>

          <div class="glass-panel" style="padding: 1rem; cursor: pointer; border-color: ${selectedYear === 2 ? 'var(--lpu-purple)' : 'var(--panel-border)'};" onclick="app.selectYear(2)">
            <div style="font-size: 0.8rem; color: #60a5fa; font-weight: 700;">YEAR 2 (Sophomore)</div>
            <div style="font-size: 1rem; font-weight: 700; margin-top: 0.2rem;">2nd Year</div>
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.4rem;">Semesters 3 & 4</div>
          </div>

          <div class="glass-panel" style="padding: 1rem; cursor: pointer; border-color: ${selectedYear === 3 ? 'var(--lpu-purple)' : 'var(--panel-border)'};" onclick="app.selectYear(3)">
            <div style="font-size: 0.8rem; color: #34d399; font-weight: 700;">YEAR 3 (Junior)</div>
            <div style="font-size: 1rem; font-weight: 700; margin-top: 0.2rem;">3rd Year</div>
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.4rem;">Semesters 5 & 6</div>
          </div>

          <div class="glass-panel" style="padding: 1rem; cursor: pointer; border-color: ${selectedYear === 4 ? 'var(--lpu-purple)' : 'var(--panel-border)'};" onclick="app.selectYear(4)">
            <div style="font-size: 0.8rem; color: #f43f5e; font-weight: 700;">YEAR 4 (Senior)</div>
            <div style="font-size: 1rem; font-weight: 700; margin-top: 0.2rem;">4th Year</div>
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.4rem;">Semesters 7 & 8</div>
          </div>
        </div>

        ${semPillHtml}
      </div>
    `;

    navContainer.innerHTML = html;
  }

  selectYear(yearNum) {
    const startTerm = (yearNum - 1) * 2 + 1;
    this.selectSemester(startTerm, yearNum);
  }

  selectSemester(semId, yearNum = null) {
    const year = yearNum || Math.ceil(parseInt(semId) / 2);
    this.renderYearNavigationCards(year, semId);

    const termSelect = document.getElementById('term-filter-select');
    if (termSelect) termSelect.value = semId;

    this.loadSubjects('', semId);
  }

  async onAnalyzerSemesterChange(semId) {
    const subjectSelect = document.getElementById('analyzer-subject-select');
    if (!subjectSelect) return;
    try {
      const subjects = await ApiService.getSubjects(null, semId || null);
      if (subjects.length > 0) {
        subjectSelect.innerHTML = subjects.map(s => `<option value="${s.subject_code}">${s.subject_code} - ${s.subject_name}</option>`).join('');
        this.openAIAnalyzer(subjects[0].subject_code);
      }
    } catch (e) {
      console.log('Error updating analyzer subjects:', e);
    }
  }

  async onMockSemesterChange(semId) {
    const subjectSelect = document.getElementById('mock-subject');
    if (!subjectSelect) return;
    try {
      const subjects = await ApiService.getSubjects(null, semId || null);
      if (subjects.length > 0) {
        subjectSelect.innerHTML = subjects.map(s => `<option value="${s.subject_code}">${s.subject_code} - ${s.subject_name}</option>`).join('');
      }
    } catch (e) {
      console.log('Error updating mock test subjects:', e);
    }
  }

  async loadSubjects(search = '', termId = null) {
    const container = document.getElementById('subjects-grid');
    if (!container) return;

    if (!document.getElementById('year-navigator-container')?.childElementCount) {
      this.renderYearNavigationCards(null);
    }

    const termSelect = document.getElementById('term-filter-select');
    const selectedTerm = termId || (termSelect ? termSelect.value : null);

    try {
      const subjects = await ApiService.getSubjects(null, selectedTerm, search);
      if (subjects.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-muted);">No subjects found for this selection.</div>';
        return;
      }
      container.innerHTML = subjects.map(s => Components.renderSubjectCard(s)).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error loading subjects: ${e.message}</div>`;
    }
  }

  filterByTerm(termId) {
    const searchVal = document.getElementById('subject-search-input')?.value || '';
    if (termId) {
      const yearNum = Math.ceil(parseInt(termId) / 2);
      this.renderYearNavigationCards(yearNum);
    } else {
      this.renderYearNavigationCards(null);
    }
    this.loadSubjects(searchVal, termId);
  }

  async openSubjectDetails(subjectCode) {
    this.activeSubject = subjectCode;
    this.switchPage('subjects');
    const container = document.getElementById('subject-detail-view');
    if (!container) return;

    try {
      const sub = await ApiService.getSubjectDetails(subjectCode);
      let html = `
        <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h2>${sub.subject_code}: ${sub.subject_name}</h2>
            <span class="badge badge-purple">${sub.program_name}</span>
          </div>
          <p style="color: var(--text-muted); font-size: 0.9rem;">${sub.description}</p>
        </div>

        <h3 style="margin-bottom: 1rem;">Authorized Academic Units & Syllabus</h3>
        <div class="grid-cards">
          ${sub.units.map(u => `
            <div class="glass-panel card-item">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge badge-blue">Unit ${u.unit_number}</span>
                <span style="font-size: 0.8rem; color: var(--accent-amber);">Exam Weight: ${u.weightage_pct}%</span>
              </div>
              <h4 style="font-size: 1.05rem;">${u.unit_title}</h4>
              <div style="margin-top: auto; display: flex; gap: 0.5rem; padding-top: 0.5rem;">
                <button class="btn btn-secondary" style="font-size: 0.75rem; flex: 1;">📑 Download Notes</button>
                <button class="btn" style="font-size: 0.75rem; flex: 1;" onclick="app.startMockTestForUnit('${sub.subject_code}', ${u.unit_id})">⚡ Practice Unit Test</button>
              </div>
            </div>
          `).join('')}
        </div>
      `;
      container.innerHTML = html;
      container.scrollIntoView({ behavior: 'smooth' });
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }

  async openAIAnalyzer(subjectCode) {
    this.activeSubject = subjectCode;
    const container = document.getElementById('ai-analysis-container');
    if (!container) return;

    container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-muted);">Analyzing syllabus and past paper frequency patterns with AI NLP Engine...</div>';

    try {
      const data = await ApiService.getAIAnalysis(subjectCode);
      let html = `
        <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
          <h3 style="color: #c084fc; margin-bottom: 0.5rem;">🤖 AI Syllabus & PYQ Topic Analysis: ${data.subject_code}</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem;">Extracted ${data.total_extracted_topics} core topic nodes from syllabus files and multi-year question papers.</p>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
          <div class="glass-panel" style="padding: 1.25rem;">
            <h4 style="margin-bottom: 1rem; color: var(--lpu-cyan);">🔥 High-Yield Exam Topics</h4>
            ${data.high_yield_topics.map(t => `
              <div style="padding: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between;">
                <div>
                  <div style="font-weight: 600; font-size: 0.9rem;">${t.topic}</div>
                  <div style="font-size: 0.75rem; color: var(--text-muted);">${t.unit}</div>
                </div>
                <div style="text-align: right;">
                  <span class="badge badge-rose">${t.frequency} PYQ Repeats</span>
                </div>
              </div>
            `).join('')}
          </div>

          <div class="glass-panel" style="padding: 1.25rem;">
            <h4 style="margin-bottom: 1rem; color: var(--accent-emerald);">📊 Unit Weightage Distribution</h4>
            ${data.unit_weightage_chart.map(w => `
              <div style="margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.25rem;">
                  <span>${w.unit}</span>
                  <strong>${w.weightage}%</strong>
                </div>
                <div style="height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden;">
                  <div style="width: ${w.weightage * 3}%; height: 100%; background: linear-gradient(90deg, #7e22ce, #3b82f6);"></div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="glass-panel" style="padding: 1.25rem;">
          <h4 style="margin-bottom: 0.75rem; color: #f59e0b;">💡 Recommended AI Revision Sequence</h4>
          <ol style="padding-left: 1.2rem; line-height: 1.8; color: var(--text-primary); font-size: 0.9rem;">
            ${data.recommended_revision_sequence.map(s => `<li>${s}</li>`).join('')}
          </ol>
        </div>
      `;
      container.innerHTML = html;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }

  async generateMockTest() {
    const subjectCode = document.getElementById('mock-subject').value;
    const numQuestions = parseInt(document.getElementById('mock-num-q').value);
    const difficulty = document.getElementById('mock-difficulty').value;

    const container = document.getElementById('mock-test-container');
    container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-muted);">Generating syllabus-aligned mock test...</div>';

    try {
      const test = await ApiService.generateAIMockTest(subjectCode, numQuestions, difficulty);
      this.currentMockQuestions = test.questions;
      this.testStartTime = new Date();

      let html = `
        <div class="glass-panel" style="padding: 1.25rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3>${test.subject_code} AI Mock Test</h3>
            <span style="font-size: 0.85rem; color: var(--text-muted);">${test.total_questions} Questions • ${test.duration_minutes} Minutes</span>
          </div>
          <button class="btn" style="background: var(--accent-emerald);" onclick="app.submitCurrentMockTest('${test.subject_code}')">✅ Submit Answers</button>
        </div>
        <form id="mock-test-form">
          ${test.questions.map((q, idx) => Components.renderQuestionCard(q, idx)).join('')}
        </form>
      `;
      container.innerHTML = html;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }

  async submitCurrentMockTest(subjectCode) {
    const form = document.getElementById('mock-test-form');
    if (!form) return;

    const answers = {};
    this.currentMockQuestions.forEach(q => {
      const selected = form.querySelector(`input[name="question_${q.question_id}"]:checked`);
      if (selected) answers[q.question_id] = selected.value;
    });

    const timeTaken = Math.round((new Date() - this.testStartTime) / 1000);

    try {
      const result = await ApiService.submitMockTest(subjectCode, answers, timeTaken);
      const container = document.getElementById('mock-test-container');

      let html = `
        <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem; text-align: center;">
          <h2 style="color: #34d399; margin-bottom: 0.5rem;">Test Result: ${result.accuracy_percentage}% Accuracy</h2>
          <p style="color: var(--text-muted);">Correct Answers: ${result.correct_answers} / ${result.total_questions} • Score: ${result.score_earned}/${result.max_possible_score}</p>
        </div>

        <h3>Question Explanations</h3>
        ${result.detailed_evaluation.map(ev => `
          <div class="glass-panel" style="padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid ${ev.is_correct ? '#10b981' : '#f43f5e'};">
            <div style="font-weight: 600; margin-bottom: 0.4rem;">${ev.question_text}</div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.4rem;">
              Your Choice: <strong style="color: ${ev.is_correct ? '#10b981' : '#f43f5e'};">${ev.user_answer || 'Skipped'}</strong> | 
              Correct Answer: <strong>${ev.correct_option}</strong>
            </div>
            <div style="font-size: 0.85rem; color: #38bdf8; background: rgba(56, 189, 248, 0.08); padding: 0.6rem; border-radius: 6px;">
              💡 <strong>Explanation:</strong> ${ev.explanation}
            </div>
          </div>
        `).join('')}
      `;
      container.innerHTML = html;
      await this.loadAnalytics();
    } catch (e) {
      alert('Error submitting test: ' + e.message);
    }
  }

  async generateStudyPlan() {
    const examDate = document.getElementById('planner-exam-date').value;
    const dailyHours = document.getElementById('planner-daily-hours').value;
    const container = document.getElementById('cpp-planner-output');

    container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-muted);">Executing C++ Max-Heap & Topological Graph Planner Engine...</div>';

    try {
      const data = await ApiService.generateStudyPlan(examDate, dailyHours);
      const schedule = data.schedule || [];

      let html = `
        <div style="margin-bottom: 1rem; color: #34d399; font-weight: 600;">
          ✅ ${data.engine} • Target Exam: ${data.exam_date} (${data.daily_hours} hrs/day)
        </div>
      `;

      html += schedule.map((item, idx) => Components.renderCppTaskNode(item, idx)).join('');
      container.innerHTML = html;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }

  async loadCAdminCLI(query = '') {
    const terminal = document.getElementById('c-cli-terminal');
    if (!terminal) return;

    terminal.innerText = 'Executing C Academic Data Manager (gcc binary)...';

    try {
      const action = query ? 'search' : 'benchmark';
      const data = await ApiService.executeCAdminCLI(action, query);
      terminal.innerText = data.stdout_output || 'No output from C binary.';
    } catch (e) {
      terminal.innerText = 'Error executing C CLI: ' + e.message;
    }
  }

  async loadAnalytics() {
    const container = document.getElementById('dashboard-analytics-content');
    if (!container) return;

    try {
      const data = await ApiService.getAnalyticsDashboard();
      const m = data.metrics;

      let html = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem;">
          <div class="glass-panel" style="padding: 1.25rem;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #c084fc;">${m.total_mock_tests_taken}</div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">Mock Tests Completed</div>
          </div>
          <div class="glass-panel" style="padding: 1.25rem;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #34d399;">${m.average_score_percentage}%</div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">Average Score Accuracy</div>
          </div>
          <div class="glass-panel" style="padding: 1.25rem;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #60a5fa;">${m.exam_readiness_score}</div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">Exam Readiness Index</div>
          </div>
        </div>

        <h3 style="margin-bottom: 1rem;">Subject Performance Breakdown</h3>
        <div class="grid-cards" style="margin-bottom: 1.5rem;">
          ${data.subject_performance.map(s => `
            <div class="glass-panel card-item">
              <div style="display: flex; justify-content: space-between;">
                <span class="badge badge-purple">${s.subject_code}</span>
                <span class="badge badge-emerald">${s.status}</span>
              </div>
              <h4>${s.subject_name}</h4>
              <div style="font-size: 0.9rem; margin-top: 0.5rem;">Average Score: <strong>${s.avg_score}%</strong></div>
            </div>
          `).join('')}
        </div>
      `;
      container.innerHTML = html;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose);">Error: ${e.message}</div>`;
    }
  }
}

const app = new LPUExamPrepApp();
