function copyIDs(m_id) {
  var code = document.getElementById(m_id);
  navigator.clipboard.writeText(code.textContent);
} 