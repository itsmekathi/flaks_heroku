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
        .controller('ListsController', ['$scope', '$log', '$mdDialog','ListDataService',
            function ($scope, $log, $mdDialog, ListDataService) {
                $log.log('Lists controller initialized');
                var self = this;
                var toastr = window.toastr;
                $scope.listTypes = [];

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

                // Add new Expense Type Dialog
                $scope.showAdvanced = function (ev) {
                    $mdDialog.show({
                        controller: 'AddNewListController',
                        templateUrl: '/static/scripts/app/lists/addlist.tmpl.html',
                        parent: angular.element(document.body),
                        targetEvent: ev,
                        clickOutsideToClose: true,
                        fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                    }).then(function (listType) {
                        self.saveListType(listType);
                    }, function () {
                        $log.log('Cancelled Save');
                    });
                };

                this.getListTypes = function(){
                    ListDataService.getListTypeLookups()
                    .then(function(response){
                        toastr.success('List type lookups fetched', 'Success');
                        $scope.listTypes = response.data;
                    }, function(error){
                        toastr.error('Failed to fetch List Types', 'Error');
                        $log.log('Error: ' + JSON.stringify(error));
                    })
                };
                this.saveListType = function(listType){
                    ListDataService.addNewListType(listType)
                        .then(function () {
                            toastr.success('New type has been updated', 'Data Saved');
                        }, function () {
                            toastr.error('Unable to save data', 'Error');
                        });
                };
                this.getListTypes();
            }]);
})();