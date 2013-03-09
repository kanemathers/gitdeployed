<div class="container-fluid">
    <div class="row-fluid">
        <div class="span3">
            <ul class="nav nav-list">
                <li data-ng-repeat="repo in repos">
                    <a title="{{repo.name}}">{{repo.name}}</a>
                </li>
            </ul>
        </div>
        <div class="span9">
        </div>
    </div>
</div>
