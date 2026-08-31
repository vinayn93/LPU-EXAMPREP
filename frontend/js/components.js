/**
 * LPU ExamPrep UI Components Renderer
 */

class Components {
  static renderSubjectCard(sub) {
    const semName = sub.semester_name || `Term ${sub.semester_id || 'Core'}`;

    return `
      <div class="glass-panel card-item">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; flex-wrap: wrap;">
          <span class="badge badge-purple">${sub.subject_code}</span>
          <span class="badge badge-blue">${semName}</span>
          <span style="font-size: 0.78rem; color: var(--text-muted);">${sub.credits} Credits</span>
        </div>
        <h3 style="font-size: 1.05rem; color: var(--text-primary); margin-top: 0.3rem;">${sub.subject_name}</h3>
        <p style="font-size: 0.83rem; color: var(--text-muted); line-height: 1.4;">${sub.description || 'Official LPU B.Tech CSE Course Module.'}</p>
        <div style="margin-top: auto; display: flex; gap: 0.5rem; padding-top: 0.75rem;">
          <button class="btn" style="flex: 1; font-size: 0.78rem;" onclick="app.openSubjectDetails('${sub.subject_code}')">📘 Study Units</button>
          <button class="btn btn-secondary" style="font-size: 0.78rem;" onclick="app.openAIAnalyzer('${sub.subject_code}')">🤖 AI PYQ Analysis</button>
        </div>
      </div>
    `;
  }

  static renderQuestionCard(q, idx) {
    return `
      <div class="glass-panel" style="padding: 1.25rem; margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
          <span style="font-weight: 700; color: var(--lpu-purple);">Question #${idx + 1} (${q.marks} Marks)</span>
          <span class="badge badge-blue">${q.difficulty}</span>
        </div>
        <p style="font-size: 0.95rem; margin-bottom: 1rem;">${q.text}</p>
        <div style="display: flex; flex-direction: column; gap: 0.6rem;">
          ${Object.entries(q.options).map(([key, val]) => `
            <label style="display: flex; align-items: center; gap: 0.6rem; background: rgba(255,255,255,0.03); padding: 0.6rem 0.8rem; border-radius: 8px; cursor: pointer;">
              <input type="radio" name="question_${q.question_id}" value="${key}">
              <span><strong>(${key})</strong> ${val}</span>
            </label>
          `).join('')}
        </div>
      </div>
    `;
  }

  static renderCppTaskNode(item, idx) {
    return `
      <div style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <span style="font-size: 1.2rem; font-weight: 800; color: #c084fc;">Day ${idx + 1}</span>
          <div>
            <div style="font-weight: 600; font-size: 0.95rem;">${item.topic_name}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">${item.subject_name} • ${item.unit_name} • Weightage ${item.unit_weightage_pct}%</div>
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 1rem; font-weight: 800; color: #f43f5e;">${item.priority_score}</div>
          <div style="font-size: 0.7rem; color: var(--text-dim);">Heap Priority Score</div>
        </div>
      </div>
    `;
  }
}
