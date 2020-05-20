(function () {
    "use strict";
    angular.module("app")
        .directive('modalWindow', function () {
            return {
                restrict: 'E',
                scope: {
                    show: '=',
                    title: '='
                },
                replace: true, // Replace with template
                transclude: true, // To use custom content
                link: function (scope, element, attrs) {
                    scope.windowStyle = {};
                    if (attrs.width) {
                        scope.windowStyle.width = attrs.width;
                    }
                    if (attrs.height) {
                        scope.windowStyle.height = attrs.height;
                    }

                    scope.hideModal = function () {
                        scope.show = false;
                    };
                },
                template: "<div ng-show='show'>\
                <div class='simple-modal-overlay' ng-click='hideModal()'>\
                </div><div class='simple-modal-background' ng-style='windowStyle'>\
                <div class='simple-modal-title'>{{title}} <span class='simple-modal-close pull-right' ng-click='hideModal()'>&times</span></div>\
                <div class='simple-modal-content' ng-transclude></div></div></div>"
            }
        })
})();