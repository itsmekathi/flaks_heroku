(function () {
    'use strict';
    angular.module('app')
        .factory('ListDataService', ['$http', '$q', '$log', 'ListConstants',
            function ($http, $q, $log, ListConstants) {
                // interface
                var service = {
                    getListTypeLookups: getListTypeLookups,
                    addNewListType: addNewListType
                }
                function getListTypeLookups() {
                    var def = $q.defer();
                    $http.get(ListConstants.ListTypeLookupsUri)
                        .then(function (response) {
                            def.resolve(response.data);
                        }, function (error) {
                            $log.log('Error occured while retrieving data.');
                            $log.log(JSON.stringify(error));
                            def.reject("Failed to get List Types");
                        });
                    return def.promise;
                };

                function addNewListType(listType) {
                    var def = $q.defer();
                    $http.post(ListConstants.ListTypeLookupsUri, listType)
                        .then(function (response) {
                            def.resolve(response.data);
                        }, function (error) {
                            $log.log('Error occured while retrieving data.');
                            $log.log(JSON.stringify(error));
                            def.reject("Failed to get List Types");
                        });
                    return def.promise;
                };
                return service;
            }]);
})();