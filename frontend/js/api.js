/**
 * LPU ExamPrep AI — REST API Client
 */

const API_BASE = '/api';

class ApiService {
  static getAuthToken() { return localStorage.getItem('lpu_token'); }
  static setAuthToken(token) { localStorage.setItem('lpu_token', token); }
  static clearAuthToken() {
    localStorage.removeItem('lpu_token');
    localStorage.removeItem('lpu_user');
  }

  static getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    const token = this.getAuthToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  }

  // Auth APIs
  static async login(email, password, registrationNumber = '') {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, registration_number: registrationNumber })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');
    this.setAuthToken(data.access_token);
    localStorage.setItem('lpu_user', JSON.stringify(data.user_profile));
    return data;
  }

  static async register(fullName, email, password, registrationNumber, programId = 1) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        full_name: fullName,
        email: email,
        password: password,
        registration_number: registrationNumber,
        program_id: parseInt(programId)
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');
    this.setAuthToken(data.access_token);
    localStorage.setItem('lpu_user', JSON.stringify(data.user_profile));
    return data;
  }

  static async oauthLogin(provider, email, fullName, registrationNumber) {
    const res = await fetch(`${API_BASE}/auth/oauth`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider: provider,
        email: email,
        full_name: fullName,
        registration_number: registrationNumber
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || `${provider} authentication failed`);
    this.setAuthToken(data.access_token);
    localStorage.setItem('lpu_user', JSON.stringify(data.user_profile));
    return data;
  }

  // Academic APIs
  static async getSubjects(programId = null, semesterId = null, search = '') {
    const params = new URLSearchParams();
    if (programId) params.append('program_id', programId);
    if (semesterId) params.append('semester_id', semesterId);
    if (search && search.trim()) params.append('search', search.trim());
    const res = await fetch(`${API_BASE}/academic/subjects?${params.toString()}`);
    return await res.json();
  }

  static async getSubjectDetails(subjectCode) {
    const res = await fetch(`${API_BASE}/academic/subjects/${subjectCode}`);
    return await res.json();
  }

  // NEW LPU MODULE APIS
  static async getSubjectDomains() {
    const res = await fetch(`${API_BASE}/academic/domains`);
    return await res.json();
  }

  static async getElectiveCategories() {
    const res = await fetch(`${API_BASE}/academic/electives`);
    return await res.json();
  }

  static async getPedagogyAndPartners() {
    const res = await fetch(`${API_BASE}/academic/pedagogy-partners`);
    return await res.json();
  }

  // AI Analysis API
  static async getAIAnalysis(subjectCode) {
    const res = await fetch(`${API_BASE}/ai/analysis/${subjectCode}`);
    return await res.json();
  }

  // AI Mock Test API
  static async generateAIMockTest(subjectCode, numQuestions = 5, difficulty = 'MEDIUM') {
    const res = await fetch(`${API_BASE}/ai/generate-test`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ subject_code: subjectCode, num_questions: numQuestions, difficulty })
    });
    return await res.json();
  }

  static async submitMockTest(subjectCode, answers, timeTakenSeconds) {
    const res = await fetch(`${API_BASE}/ai/submit-test`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ subject_code: subjectCode, answers, time_taken_seconds: timeTakenSeconds })
    });
    return await res.json();
  }

  // C++ Study Planner API
  static async generateStudyPlan(examDate, dailyHours) {
    const res = await fetch(`${API_BASE}/study-plan/generate`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ exam_date: examDate, available_hours_per_day: parseFloat(dailyHours) })
    });
    return await res.json();
  }

  // C Admin CLI API
  static async executeCAdminCLI(action = 'benchmark', searchQuery = '') {
    let url = `${API_BASE}/admin-cli/execute?action=${action}`;
    if (searchQuery) url += `&search_query=${encodeURIComponent(searchQuery)}`;
    const res = await fetch(url, { headers: this.getHeaders() });
    return await res.json();
  }

  // Analytics API
  static async getAnalyticsDashboard() {
    const res = await fetch(`${API_BASE}/analytics/dashboard`, { headers: this.getHeaders() });
    return await res.json();
  }
}
