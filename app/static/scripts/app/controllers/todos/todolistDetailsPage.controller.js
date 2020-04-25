(function () {
    'use strict';

    angular.module('app')
        .controller('todoListDetailsController', ['$scope', '$log', '$mdDialog', '$http', '$window',
            function ($scope, $log, $mdDialog, $http, $window) {
                $log.log('Todo List details controller initialized');
                $scope.status = '  ';
                $scope.todoItemUrl = '/api/v1/todo_item/'
                $scope.todoListUrl = '/api/v1/todo_list'

                $scope.deleteMethod = 'DELETE';
                $scope.getMethod = 'GET';
                $scope.putMethod = 'PUT';

                $scope.currentToDoListId = null;    // Will be set by the ng-oninit on the view 
                $scope.currentItemId = 0;
                $scope.selectedItems = [];
                $scope.selectedItemId = null;
                $scope.userToDoLists = [];
                $scope.selectedList = null;

                // Add items to array
                $scope.itemSelected = function (todoitem_id) {
                    if ($scope.selectedItems.findIndex(_ => _ == todoitem_id) >= 0) {
                        var index = $scope.selectedItems.findIndex(_ => _ == todoitem_id);
                        $scope.selectedItems.splice(index, 1);
                    } else {
                        $scope.selectedItems.push(todoitem_id);
                    }
                };
                // Move the todo item
                $scope.moveItemDialog = function (todoitem_id, $event) {
                    $log.log('Initiated move of item ' + todoitem_id);
                    $scope.selectedItemId = todoitem_id;
                    $scope.selectedList = null;
                    $mdDialog.show({
                        contentElement: '#moveTodoItemDialog',
                        parent: angular.element(document.body)
                    });
                };

                // Move item action
                $scope.moveTodoItem = function () {
                    $log.log('Move todo item initiated');
                    $http({
                        method: $scope.putMethod,
                        url: $scope.todoItemUrl + 'move',
                        data: {
                            todoItemId: $scope.selectedItemId,
                            todoListId: $scope.selectedList.body.id
                        }
                    }).then(function (response) {
                        $log.log('Item moved succesfully');
                        $log.log(response);
                        $scope.closeMoveItemDialog();
                        $window.location.reload();
                    }, function (response) {
                        $log.log('Error moving item.');
                        $log.log(response);
                        $scope.closeMoveItemDialog();
                    });
                };

                $scope.closeMoveItemDialog = function () {
                    $mdDialog.hide();
                }

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
                        deleteItem();
                    }, function () {
                        $log.log('Cancel action initialted');
                    });
                };

                var fetchToDoList = function () {
                    $http({
                        method: $scope.getMethod,
                        url: $scope.todoListUrl
                    }).then(function (response) {
                        $scope.userToDoLists = response.data.todolists
                            .filter(_ => _.body.id !== $scope.currentToDoListId);
                    }, function (response) {
                        $log.log('Error fetching todoLists for user');
                        $log.log(response);
                    });
                };

                fetchToDoList();

                var deleteItem = function () {
                    $http({
                        method: $scope.deleteMethod,
                        url: $scope.todoItemUrl + $scope.currentItemId
                    }).then(function (response) {
                        $scope.status = response.status;
                        $window.location.reload();
                    }, function (response) {
                        $scope.data = response.data.posts || 'Request failed';
                        $scope.status = response.status;
                    });
                };
            }]);
})()