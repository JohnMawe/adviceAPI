const sidebarItems = document.querySelectorAll(".sidebar-item");
const exploreViews = document.querySelectorAll(".explore-view");


sidebarItems.forEach((item) => {

    item.addEventListener("click", () => {

        const viewName = item.dataset.view;

        if (!viewName) {
            return;
        }


        // Update active sidebar button

        sidebarItems.forEach((button) => {
            button.classList.remove("active");
        });

        item.classList.add("active");


        // Show selected view

        exploreViews.forEach((view) => {
            view.hidden = view.id !== `${viewName}-view`;
        });

    });

});