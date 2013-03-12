angular.module('gitdeployed.directives', [])

.directive('btnDelete', [
    '$q',
    '$timeout',

    function($q, $timeout)
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
                var confirm = function()
                {
                    var deferred = $q.defer();
                    var ticks    = 3
                    var btnText  = tickText(ticks);
                    var timer    = {
                        confirm: null,
                        pending: null
                    };

                    var clickFn = function()
                    {
                        clearTimeout(timer.pending);

                        element
                            .unbind('click.tmp')
                            .removeClass('btn-danger');

                        scope.$apply(deferred.resolve);
                    };

                    var tick = function()
                    {
                        element.text(btnText());

                        if (--ticks !== 0)
                            return;

                        clearInterval(timer.confirm);

                        element
                            .removeClass('disabled')
                            .bind('click.tmp', clickFn);

                        timer.pending = setTimeout(function()
                        {
                            element
                                .unbind('click.tmp')
                                .removeClass('btn-danger');

                            scope.$apply(deferred.reject);
                        }, 5000);
                    };

                    element
                        .addClass('disabled btn-danger')
                        .text(btnText());

                    timer.confirm = setInterval(tick, 1000);

                    return deferred.promise;
                };

                element.click(function()
                {
                    if (element.hasClass('btn-danger'))
                        return;

                    confirm().then(function()
                    {
                        scope.btnDelete();
                    });
                });
            }
        };
    }
]);
