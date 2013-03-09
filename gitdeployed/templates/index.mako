<!DOCTYPE html>
<html lang="en" data-ng-app="gitdeployed">
<head>
    <meta charset="utf-8">
    <title>gitdeployed</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="Kane Mathers">

    % for url in request.webassets_env['less'].urls():
    <link href="${url}" rel="stylesheet">
    % endfor

    <!--[if lt IE 9]>
        <script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
</head>
<body>
    <div data-ng-view></div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.4/angular.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.4/angular-resource.min.js"></script>

    % for url in request.webassets_env['js'].urls():
    <script src="${url}"></script>
    % endfor
</body>
</html>
