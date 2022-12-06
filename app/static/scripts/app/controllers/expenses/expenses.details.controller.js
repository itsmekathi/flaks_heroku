(function () {
    'use strict';
    angular.module('app')
        .controller('expensesDetailsController', ['$log', '$mdDialog', '$window', 'ExpensesDataService', 'ExpensesConstants', 'ToastrService',
            function ($log, $mdDialog, $window, expensesDataService, expensesConstants, ToastrService) {
                var self = this;

                self.isShowExpenseItemAddModal = false;
                self.isShowExpenseItemEditModal = false;
                self.total = 0;
                self.expensesDetails = [];

                self.showConfirm = function (ev, deleteUrl) {
                    var confirm = $mdDialog.confirm()
                        .title('Would you like to delete this item')
                        .textContent('This is an Irreversible action')
                        .targetEvent(ev)
                        .ok('Delete')
                        .cancel('Cancel');

                    $mdDialog.show(confirm).then(function () {
                        $log.log('Delete item action initialted');
                        expensesDataService.deleteItem(deleteUrl)
                            .then(function (data) {
                                getDetails();
                                ToastrService.showSuccess(data.status, 'Deleted item');
                            }, function (error) {
                                ToastrService.showError('Error', error.statusText);
                            });
                    }, function () {
                        $log.log('Cancel action initialted');
                    });
                };

                function calcuateTotal() {
                    if (self.expensesDetails != null && self.expensesDetails.length > 0) {
                        for (let i = 0; i < self.expensesDetails.length; i++) {
                            self.total += parseInt(self.expensesDetails[i].grossPrice);
                        }
                    } else {
                        self.total = 0;
                    }
                };

                function getDetails() {
                    expensesDataService.getExpensesDetails()
                        .then(function (data) {
                            self.expensesDetails = data.expenseItems;
                            calcuateTotal();
                        }, function (error) {
                            ToastrService.showError('Error', error.statusText)
                        })
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
                            self.isShowExpenseItemAddModal = false;
                            getDetails();
                        }).fail(function (error) {
                            $log.log('Error: Enter valid values')
                            ToastrService.showWarning('Enter valid data in the form', 'Invalid data');
                            $('.add-expense-item-form-wrapper').empty().append($(error.responseText).hide().fadeIn(500));
                            addEventListeners();
                        });
                    });
                }

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
                            self.isShowExpenseItemEditModal = false;
                            getDetails();
                        }).fail(function (error) {
                            $log.log('Error: Enter valid values')
                            ToastrService.showWarning('Enter valid data in the form', 'Invalid data');
                            $('.edit-expenseitem-form-wrapper').empty().append($(error.responseText).hide().fadeIn(500));
                            addEditEventListeners();
                        });
                    });
                };

                self.showExpenseModal = function () {
                    expensesDataService.getFormTemplate(expensesConstants.AddExpenseDetailFormUrl)
                        .then(function (data) {
                            $('.add-expense-item-form-wrapper').empty().append($(data).hide().fadeIn(500));
                            self.isShowExpenseItemAddModal = true;
                            addEventListeners();
                        }, function (error) {
                            ToastrService.showError('Error', error.statusText);
                        });
                };
                self.showEditExpenseItemModal = function (editUrl) {
                    expensesDataService.getFormTemplate(editUrl)
                        .then(function (data) {
                            $('.edit-expenseitem-form-wrapper').empty().append($(data).hide().fadeIn(500));
                            self.isShowExpenseItemEditModal = true;
                            addEditEventListeners();
                        }, function (error) {
                            ToastrService.showError('Error', error.statusText);
                            self.isShowExpenseItemEditModal = false;
                        });
                };

                getDetails();
            }]);
})();