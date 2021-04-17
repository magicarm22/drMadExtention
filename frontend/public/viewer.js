
let token = '';
let tuid = '';

const twitch = window.Twitch.ext;

// create the request options for our Twitch API calls
const requests = {
  set: createRequest('POST', 'cycle'),
  get: createRequest('GET', 'query')
};

const utilsRequests = {
  getNameById: createRequest('GET', 'getNameById')
}

const userInformation = {
  getInfo: createRequest('GET', 'info')
};

var header = {
  timeout: null,
  // 헤더를 가린다 (마우스 나갈 때)
  disable: function disable() {
    if (this.timeout !== null) {
      clearTimeout(this.timeout);
    }

    this.timeout = setTimeout(function () {
      $('body').removeClass('init');
      bodyToggle.visible(false);
    }, 1);
  },
  // 헤더를 보이게 한다 (마우스 나갈 때)
  enable: function enable() {
    if (this.timeout !== null) {
      clearTimeout(this.timeout);
    }

    this.timeout = setTimeout(function () {
      $('body').removeClass('init');
      bodyToggle.visible(true);
    }, 1);
  }
};

var bodyToggle = {
  visible: function visible() {
    var isEnable = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null;

    var body = $('.main_window');
    console.log(body);
    body.toggleClass('visible-enabled', isEnable).toggleClass('visible-disabled', !body.hasClass('visible-enabled'));
  }
};

function createRequest (type, method) {
  return {
    method: type,
    url: location.protocol + '//localhost:8000/drmad/' + method,
  };
}

function setAuth (request, token) {
  Object.keys(request).forEach((req) => {
    twitch.rig.log('Setting auth headers');
    request[req].headers = { 'Authorization': 'Bearer ' + token };
  });
}

twitch.onContext(function (context) {
  twitch.rig.log(context);
});

twitch.onAuthorized(function (auth) {
  // save our credentials
  token = auth.token;
  console.log(token)
  clientId = auth.clientId;
  tuid = auth.userId;


  // enable the button
  $('#cycle').removeAttr('disabled');

  setAuth(requests, token);
  setAuth(userInformation, token);
  setAuth(utilsRequests, token);
  console.log(token);
  // $.ajax(requests.get);
  // utilsRequests.params = {
  //   "clientId": clientId,
  //   "userId": tuid
  // };
  axios(utilsRequests).then(res => console.log(res))
});

function updateBlock (hex) {
  twitch.rig.log('Updating block color');
  $('#color').css('background-color', hex);
}

function logError(_, error, status) {
  twitch.rig.log('EBS request returned '+status+' ('+error+')');
}

function logSuccess(hex, status) {
  twitch.rig.log('EBS request returned '+hex+' ('+status+')');
}


$(function () {
  // when we click the cycle button
  $('#cycle').click(function () {
  if(!token) { return twitch.rig.log('Not authorized'); }
  });
  // $('body').on('mouseenter mouseover', function () {
  //     header.enable();
  //   }).on('mouseleave mouseout', function () {
  //     header.disable();
  //   }).addClass('init');
  $('.mini_button').click(function (e) {
    e.preventDefault();
    e.stopPropagation();

    twitch.rig.log('GetUserInfo');
    req = userInformation.getInfo;

    req.params = {username: twitch.name};
    axios(req).then( res =>
        console.log(res)
    );
    bodyToggle.visible();


  })
});
