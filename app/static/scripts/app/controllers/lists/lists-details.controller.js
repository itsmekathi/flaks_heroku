(function () {
    'use strict';
    angular.module('app')
        .controller('ListsDetailsController', ['$scope', '$log', '$mdDialog', 'ListDataService', 'ToastrService',
            function ($scope, $log, $mdDialog, ListDataService, ToastrService) {
                $log.log('Lists Details controller initialized');
                var self = this;
                self.listData = {};

                self.gridOptions = {
                    enableSorting: false,
                    columnDefs: [
                        { field: 'name' },
                        { field: 'description' },
                        { field: 'stars', enableSorting: true, type: 'number' },
                        { field: 'sortOrder', enableSorting: true, type: 'number' },
                        ,
                        {
                            field: 'Actions',
                            cellTemplate:
                                `<span><a href="#" ng-click="grid.appScope.showConfirm($event, row.entity )" class="btn"
                        title="Delete Item"><i class="fas fa-trash-alt" style="color:red;"></i></a></span>`
                        }
                    ],
                    onRegisterApi: function (gridApi) {
                        $scope.gridApi = gridApi;
                        gridApi.rowEdit.on.saveRow($scope, self.saveRow);
                    }
                };

                self.saveRow = function (listDetail) {
                    var promise = ListDataService.updateListDetail(listDetail);
                    $scope.gridApi.rowEdit.setSavePromise(listDetail, promise);
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
                        ListDataService.deleteListItem($scope.currentItem)
                            .then(function (data) {
                                ToastrService.showSuccess('Item deleted successfully', 'Success');
                                self.getListDetails();
                            }, function () {
                                $log.log('Delete action Failed');
                            });
                    }, function () {
                        $log.log('Cancel action initialted');
                    });
                };


                self.getListDetails = function () {
                    ListDataService.getListDetails()
                        .then(function (data) {
                            self.listData = data.listData
                            self.gridOptions.data = data.listData.listItems;
                        }, function () {
                            ToastrService.showError('Failed to fetch List Items', 'Error');
                        })
                };

                self.addListItemDetails = function (listType) {
                    ListDataService.addNewListType(listType)
                        .then(function (data) {
                            ToastrService.showSuccess('New type has been updated', 'Data Saved');
                            $self.listTypes.push(data);
                            self.listTypesCopy.push(data);
                        }, function () {
                            ToastrService.showError('Unable to save data', 'Error');
                        });
                };
                self.getListDetails();
            }]);
})();