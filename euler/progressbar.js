function updateProgressBar() {
    var completedElements = document.querySelectorAll('td.completed').length;
    var totalElements = document.querySelectorAll('td').length;
    var progressBar = document.getElementById('progressBar');
    if (!progressBar) { return; }
    var percentage = totalElements ? (completedElements / totalElements) * 100 : 0;
    progressBar.style.width = percentage + '%';
    progressBar.textContent = percentage.toFixed(1) + '%';
    var container = progressBar.closest('[role="progressbar"]');
    if (container) {
        container.setAttribute('aria-valuemin', '0');
        container.setAttribute('aria-valuemax', '100');
        container.setAttribute('aria-valuenow', percentage.toFixed(1));
    }
}
window.onload = function() {
    updateProgressBar();
};
