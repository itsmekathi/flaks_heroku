(function () {
    "use strict";
    angular.module("app")
        .controller("allListsController", ['ModalService', function (ModalService, modal) {
            var vm = this;
            vm.title = "AllListsController";
            vm.openModal = openModal;
            vm.closeModal = closeModal;

            function openModal(id) {
                console.log("Opening modal with id: " + id);
                ModalService.Open(id);
            }
            function closeModal(id) {
                console.log("Closing modal with id: " + id);
                ModalService.Close(id);
            }
        }]);
})();