(function () {
    'use strict';
    angular.module('app')
        .controller('AddNewListController', ['$scope', '$mdDialog',
            function ($scope, $mdDialog) {
                $scope.cancel = function () {
                    $mdDialog.cancel();
                };

                $scope.save = function () {
                    $mdDialog.hide($scope.list);
                };
            }])
        .controller('ListsController', ['$scope', '$log', '$mdDialog', 'ListDataService', 'ToastrService',
            function ($scope, $log, $mdDialog, ListDataService, ToastrService) {
                $log.log('Lists controller initialized');
                var self = this;
                $scope.listTypes = [];

                $scope.gridOptions = {
                    enableSorting: false,
                    columnDefs: [
                        { field: 'name' },
                        { field: 'description' },
                        { field: 'icon' },
                        { field: 'styleClass' },
                        { field: 'sortOrder', enableSorting: true, type: 'number' }
                    ],
                    onRegisterApi: function (gridApi) {
                        $scope.gridApi = gridApi;
                        gridApi.rowEdit.on.saveRow($scope, $scope.saveRow);
                    }
                };

                $scope.saveRow = function (rowEntity) {
                    console.log("Save initiated");
                    console.log(JSON.stringify(rowEntity));
                }

                // Angular material dialog
                $scope.showConfirm = function (ev, item) {
                    $scope.currentItem = item;
                    var confirm = $mdDialog.confirm()
                        .title('Would you like to delete this item')
                        .textContent('This is an Irreversible action')
                        .targetEvent(ev)
                        .ok('Delete')
                        .cancel('Cancel');

                    $mdDialog.show(confirm).then(function () {
                        ListDataService.deleteListType($scope.currentItem.resourceUri)
                            .then(function (data) {
                                ToastrService.showSuccess('Item deleted successfully', 'Success');
                                self.getListTypes();
                            }, function () {
                                $log.log('Delete action Failed');
                            });
                    }, function () {
                        $log.log('Cancel action initialted');
                    });
                };

                // Add new Expense Type Dialog
                $scope.showAdvanced = function (ev) {
                    $mdDialog.show({
                        controller: 'AddNewListController',
                        templateUrl: '/static/scripts/app/controllers/lists/addlist.tmpl.html',
                        parent: angular.element(document.body),
                        targetEvent: ev,
                        clickOutsideToClose: true,
                        fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                    }).then(function (listType) {
                        self.addListType(listType);
                    }, function () {
                        $log.log('Cancelled Save');
                    });
                };

                // Save the edited list type
                $scope.saveItem = function (listTypeItem) {
                    ListDataService.saveListType(listTypeItem)
                        .then(function (data) {
                            ToastrService.showSuccess('Updated item', 'Success');
                            self.getListTypes();
                        }, function (error) {
                            ToastrService.showError('Error updating item', 'Error');
                        });
                }

                self.getListTypes = function () {
                    ListDataService.getListTypeLookups()
                        .then(function (data) {
                            $scope.listTypes = data;
                            $scope.gridOptions.data = data;
                        }, function () {
                            ToastrService.showError('Failed to fetch List Types', 'Error');
                        })
                };

                self.addListType = function (listType) {
                    ListDataService.addNewListType(listType)
                        .then(function (data) {
                            ToastrService.showSuccess('New type has been updated', 'Data Saved');
                            $scope.listTypes.push(data);
                            self.listTypesCopy.push(data);
                        }, function () {
                            ToastrService.showError('Unable to save data', 'Error');
                        });
                };
                self.getListTypes();
            }]);
})();