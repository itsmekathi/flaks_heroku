(function () {
    'use strict';
    angular.module('app')
        .factory('ExpensesDataService', ['$http', '$q', '$log','ExpensesConstants',
            function ($http, $q, $log, expensesConstants) {
                // interface
                var service = {
                    getExpensesDetails: getExpensesDetails,
                    getItemEditForm: getItemEditForm,
                    deleteItem: deleteItem,
                };
                function getExpensesDetails() {
                    $log.log('Fetching Expenses Details');
                    var def = $q.defer();
                    $http.get(expensesConstants.ExpenseDetailsUrl)
                        .then(function (response) {
                            def.resolve(response.data);
                        }, function (error) {
                            def.reject(error);
                        });
                    return def.promise;
                };
                function deleteItem(url){
                    $log.log('Fetching Edit template from url: ' + url);
                    var def = $q.defer();
                    $http.delete(url)
                        .then(function (response) {
                            def.resolve(response.data);
                        }, function (error) {
                            def.reject(error);
                        });
                    return def.promise;
                }
                function getItemEditForm(url){
                    $log.log('Fetching Edit template from url: ' + url);
                    var def = $q.defer();
                    $http.get(url)
                        .then(function (response) {
                            def.resolve(response.data);
                        }, function (error) {
                            def.reject(error);
                        });
                    return def.promise;
                }
                return service;
            }]);
})();