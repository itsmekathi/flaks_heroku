(function () {
    "use strict";
    angular.module("app")
        .factory('modal', ['$compile', '$rootScope', function ($compile, $rootScope) {
            return function () {
                var elm;
                var modal = {
                    open: function () {
                        var html = `<div class="modal" ng-style="modalStyle">{{modalStyle}}
                        <div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                        </div><div class="modal-body">
                        <ng-transclude></ng-transclude>
                        </div>
                        </div>
                        <div class="modal-footer">
                         <button id="buttonClose" class="btn btn-primary" ng-click="close()">Close</button>
                        </div>
                        </div>
                        </div>
                        </div>`;
                        elm = angular.element(html);
                        angular.element(document.body).prepend(elm);

                        $rootScope.close = function () {
                            modal.close();
                        };

                        $rootScope.modalStyle = { "display": "block" };

                        $compile(elm)($rootScope);
                    },
                    close: function () {
                        if (elm) {
                            elm.remove();
                        }
                    }
                };
                return modal;
            };
        }]);
})();