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
                        { field: 'sortOrder', enableSorting: true, type: 'number' }
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