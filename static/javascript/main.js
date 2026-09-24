document.addEventListener('DOMContentLoaded', function () {
    const notify = document.getElementById('riderNotify');
    if (!notify) return;

    setInterval(function () {
        fetch('/accounts/rider-alerts/')
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.count > 0) {
                    notify.innerHTML = '<a href="/accounts/rider-dashboard/">' + data.count + ' new service request(s) — Accept or Decline</a>';
                } else {
                    notify.innerHTML = '<span>No new service notifications</span>';
                }
            })
            .catch(function () {});
    }, 8000);
});
