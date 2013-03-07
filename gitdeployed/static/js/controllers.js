angular.module('gitdeployed.controllers', [
    'gitdeployed.services'
])

.controller('ReposCtrl', [
    '$scope',
    'Repos',

    function($scope, Repos)
    {
        alert(1);
    }
]);
