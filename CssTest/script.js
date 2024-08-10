document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('.tab-button');
    const subTabButtons = document.querySelectorAll('.sub-tab-button');

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(button.getAttribute('data-tab')).classList.add('active');
            
            // Reset sub-tabs when switching main tabs
            document.querySelector(`#${button.getAttribute('data-tab')} .sub-tab-button`).click();
        });
    });

    subTabButtons.forEach(button => {
        button.addEventListener('click', function () {
            const parentTab = button.closest('.tab-content');
            const subTabContents = parentTab.querySelectorAll('.sub-tab-content');
            const siblingButtons = parentTab.querySelectorAll('.sub-tab-button');

            siblingButtons.forEach(btn => btn.classList.remove('active'));
            subTabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(button.getAttribute('data-subtab')).classList.add('active');
        });
    });

    // Initialize the first tab and sub-tab as active
    document.querySelector('.tab-button.active').click();
});
