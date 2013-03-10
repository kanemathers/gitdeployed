angular.module('gitdeployed.directives', [])

.directive('btnDelete', [
    '$timeout',

    function($timeout)
    {
        var tickText = function(total)
        {
            return function()
            {
                return (!total) ? 'Delete' :  'Really? (' + total-- + ')';
            };
        };

        return {
            restrict: 'A',
            scope:    {
                btnDelete: '&'
            },
            link: function(scope, element, attrs)
            {
                var ticks   = 3;
                var btnText = tickText(ticks);
                var ticker  = null;

                var tick = function()
                {
                    element.text(btnText());

                    if (!--ticks)
                    {
                        clearInterval(ticker);
                        activateDelete();
                    }
                };

                var deleteCallback = function()
                {
                    resetBtn();
                    scope.btnDelete();
                };

                var activateDelete = function()
                {
                    $timeout(resetBtn, 5000);

                    element
                        .removeClass('disabled')
                        .click(deleteCallback);
                };

                var resetBtn = function()
                {
                    ticks   = 3;
                    btnText = tickText(ticks);

                    element
                        .removeClass('btn-danger')
                        .text('Delete')
                        .unbind('click', deleteCallback);

                    clearInterval(ticker);
                };

                element.click(function()
                {
                    element
                        .addClass('btn-danger disabled')
                        .text(btnText());

                    ticker = setInterval(function()
                    {
                        scope.$apply(tick);
                    }, 1000);
                });
            }
        };
    }
]);
