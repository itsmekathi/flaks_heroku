(function () {
    'use strict';
    angular.module('app')
        .controller('expensesDetailsController', ['$scope', '$log', '$mdDialog', '$http', '$window', 'ToastrService',
            function ($scope, $log, $mdDialog, $http, $window, ToastrService) {
                var self = this;

                self.isShowExpenseItemAddModal = false;
                self.isShowExpenseItemEditModal = false;

                $scope.showConfirm = function (ev, deleteUrl) {
                    var confirm = $mdDialog.confirm()
                        .title('Would you like to delete this item')
                        .textContent('This is an Irreversible action')
                        .targetEvent(ev)
                        .ok('Delete')
                        .cancel('Cancel');

                    $mdDialog.show(confirm).then(function () {
                        $log.log('Delete item action initialted');
                        deleteItem(deleteUrl);
                    }, function () {
                        $log.log('Cancel action initialted');
                    });
                };

                var deleteItem = function (url) {
                    $http({
                        method: 'DELETE',
                        url: url
                    }).then(function (response) {
                        $scope.status = response.status;
                        $window.location.reload();
                    }, function (response) {
                        ToastrService.showError('Error', response.statusText);
                    });
                };

                function addEventListeners() {
                    $(".add-expense-detail-form").submit(function (event) {
                        event.preventDefault();
                        var form = $(this);
                        $.ajax({
                            type: form.attr("method"),
                            url: form.attr("action"),
                            data: form.serialize()
                        }).done(function (data) {
                            $log.log(data);
                            ToastrService.showSuccess('Added items successfully', 'Item added');
                            $window.location.reload();
                        }).fail(function (error) {
                            $log.log('Error: Enter valid values')
                            ToastrService.showWarning('Enter valid data in the form', 'Invalid data');
                            $('.add-expenseitem-form-wrapper').empty().append($(error.responseText).hide().fadeIn(500));
                            addEventListeners();
                        });
                    });
                }

                function getEditModalView(editItemUrl) {
                    $http({
                        method: 'GET',
                        url: editItemUrl
                    }).then(function (response) {
                        $('.edit-expenseitem-form-wrapper').empty().append($(response.data).hide().fadeIn(500));
                        self.isShowExpenseItemEditModal = true;
                        addEditEventListeners();
                    }, function (error) {
                        ToastrService.showError('Error', error.statusText);
                        self.isShowExpenseItemEditModal = false;
                    })
                };


                function addEditEventListeners() {
                    $(".edit-expense-item-form").submit(function (event) {
                        event.preventDefault();
                        var form = $(this);
                        $.ajax({
                            type: form.attr("method"),
                            url: form.attr("action"),
                            data: form.serialize()
                        }).done(function (data) {
                            $log.log(data);
                            ToastrService.showSuccess('Item edited successfully', 'Edit success');
                            $window.location.reload();
                        }).fail(function (error) {
                            $log.log('Error: Enter valid values')
                            ToastrService.showWarning('Enter valid data in the form', 'Invalid data');
                            $('.edit-expenseitem-form-wrapper').empty().append($(error.responseText).hide().fadeIn(500));
                            addEditEventListeners();
                        });
                    });
                };

                self.showExpenseModal = function () {
                    self.isShowExpenseItemAddModal = true;
                    addEventListeners();
                };
                self.showEditExpenseItemModal = function (editUrl) {
                    getEditModalView(editUrl);
                };
            }]);
})();