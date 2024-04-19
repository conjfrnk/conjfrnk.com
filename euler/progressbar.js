function updateProgressBar() {
    var completedElements = document.querySelectorAll('td.completed').length;
    var totalElements = document.querySelectorAll('td').length;
    var progressBar = document.getElementById('progressBar');
    var percentage = (completedElements / totalElements) * 100;
    progressBar.style.width = percentage + '%';
    progressBar.textContent = percentage.toFixed(1) + '%';
}
window.onload = function() {
    updateProgressBar();
};
