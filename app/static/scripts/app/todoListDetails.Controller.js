(function () {
    'use strict';
    angular.module('app')
        .controller('todoListDetailsController', ['$scope', '$log', '$mdDialog',
            function ($scope, $log, $mdDialog) {
                $log.log('Todo List details controller initialized');
                $scope.status = '  ';
                $scope.customFullscreen = false;

                // Angular material dialog
                $scope.showConfirm = function (ev) {
                    var confirm = $mdDialog.confirm()
                        .title('Would you like to delete this item')
                        .textContent('This is an Irreversible action')
                        .targetEvent(ev)
                        .ok('Delete')
                        .cancel('Cancel');

                    $mdDialog.show(confirm).then(function () {
                        $log.log('Delete item action initialted');
                    }, function () {
                        $log.log('Cancel action initialted');
                    });
                };
            }]);
})()