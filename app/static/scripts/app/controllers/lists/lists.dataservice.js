(function () {
    'use strict';
    angular.module('app')
        .factory('ListDataService', ['$http', '$q', '$log', 'ListConstants',
            function ($http, $q, $log, ListConstants) {
                // interface
                var service = {
                    saveListType: saveListType,
                    getListTypeLookups: getListTypeLookups,
                    addNewListType: addNewListType,
                    deleteListType: deleteListType
                };
                function saveListType(listType) {
                    var def = $q.defer();
                    $http.post(listType.resourceUri, listType)
                        .then(function (response) {
                            def.resolve(response.data);
                        }, function (error) {
                            def.reject(error);
                        });
                    return def;
                };
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
                function deleteListType(url) {
                    var def = $q.defer();
                    $http.delete(url)
                        .then(function (response) {
                            def.resolve(response.data);
                        }, function (error) {
                            def.reject(error);
                            $log.log(JSON.stringify(error));
                        });
                    return def.promise;
                };
                return service;
            }]);
})();