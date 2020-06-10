// toast angular service wrapper at application level
// implement abstractions based on https://github.com/CodeSeven/toastr

(function () {
    'use strict';
    angular.module('app')
        .factory('ToastrService', [
            function () {
                var self = this;
                self.toastr = window.toastr;
                self.toastr.options.closeButton = true;
                self.toastr.options.closeMethod = 'fadeOut';
                self.toastr.options.closeDuration = 300;
                self.toastr.options.closeEasing = 'swing';
                toastr.options.progressBar = true;


                // Interface
                var service = {
                    showInformation: showInformation,
                    showWarning: showWarning,
                    showSuccess: showSuccess,
                    showError: showError,
                    remove: remove,
                    clear: clear
                }
                // Show information
                function showInformation(message) {
                    self.toastr.info(message);
                };
                // Show warning message
                function showWarning(message) {
                    self.toastr.warning(message);
                };

                // Display a success toast, with a title
                function showSuccess(message, title) {
                    self.toastr.success(message, title);
                };

                // Display an error toast, with a title
                function showError(message, title) {
                    self.toastr.error(message, title);
                };

                // Immediately remove current toasts without using animation
                function remove() {
                    self.toastr.remove();
                };
                // Remove current toasts using animation
                function clear() {
                    self.toastr.clear();
                };

                return service;
            }]);
})();