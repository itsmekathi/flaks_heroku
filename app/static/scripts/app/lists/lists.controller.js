(function () {
    'use strict';
    angular.module('app')
        .controller('AddNewListController', ['$scope', '$mdDialog', 'ListDataService',
            function ($scope, $mdDialog, ListDataService) {
                $scope.fullscreen = true;
                var toastr = window.toastr;
                var self = this;
                $scope.hide = function () {
                    $mdDialog.hide();
                };
                $scope.cancel = function () {
                    $mdDialog.cancel();
                };

                $scope.save = function () {
                    self.addNew($scope.list);
                };

                self.addNew = function (listType) {
                    ListDataService.addNewListType(listType)
                        .then(function () {
                            toastr.success('New status updated', 'Data Saved');
                            $mdDialog.hide(JSON.stringify($scope.list));
                        }, function () {
                            toastr.error('Unable to save data', 'Error');
                            $mdDialog.hide(JSON.stringify($scope.list));
                        });
                };
            }])
        .controller('ListsController', ['$scope', '$log', '$mdDialog',
            function ($scope, $log, $mdDialog) {
                $log.log('Lists controller initialized');

                // Angular material dialog
                $scope.showConfirm = function (ev, itemId) {
                    $scope.currentItemId = itemId;
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

                // Add new Expense Type
                $scope.showAdvanced = function (ev) {
                    $mdDialog.show({
                        controller: 'AddNewListController',
                        templateUrl: '/static/scripts/app/lists/addlist.tmpl.html',
                        parent: angular.element(document.body),
                        targetEvent: ev,
                        clickOutsideToClose: true,
                        fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                    }).then(function (answer) {
                        $log.log('New item is added');
                    }, function () {
                        $log.log('Cancelled');
                    });
                };
            }]);
})();