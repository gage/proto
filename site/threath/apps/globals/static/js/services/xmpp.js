app.service('xmpp', ['$rootScope', '$window', '$http', function($rootScope, $window, $http){

    var xmpp = this;

    $window.addEventListener('online', function(){
        xmpp.reconnect();
    });

    $window.addEventListener('offline', function(){
        xmpp.disconnect();
    });

    var conn = null, pingTimer = null,
        checkConnTimer = null;

    xmpp.getConnection = function(){
        return conn;
    };

    xmpp.scope = $rootScope.$new(true);
    xmpp.getScope = function(){
        return xmpp.scope;
    };

    xmpp.initScope = function(){
        angular.extend(xmpp.scope, {
            user_id: '',
            phone_id: '',
            username: '',
            host: '',
            muc_host: '',
            sid: '',
            rid: '',
            jid: '',
            http_bind_url: '',
            ws_bind_url: '',
            resource: 'WEB:'+Math.uuid().substr(-10),
            join_rooms: {},
            last_ping: '',
            connected: false,
            reconnect: false,
            logout: true
        });
    };

    xmpp.scope.$watch('sid', _.throttle(_.bind(function(newValue, oldValue){
        if(!xmpp.scope.connecting && newValue != ''){
            console.log(newValue, oldValue);
            xmpp.scope.connecting = true;
            xmpp.connect();
        }
    },this),200));

    xmpp.uniqueID = 0;

    xmpp.getUniqueId = function(){
        return ++xmpp.uniqueID;
    };

    xmpp.updateScope = function(data){
        angular.extend(xmpp.scope, data);
    };

    xmpp.onConnected = function(s){console.log('onConnected', s)};

    xmpp.init = function(xmppData, call_back){
        if(xmpp.scope.connected){
            return false;
        }
        xmpp.initScope();
        if(call_back && typeof call_back == 'function'){
            xmpp.onConnected = call_back;
        }
        if(xmppData){
            xmpp.updateScope({
                user_id: xmppData.conn.user_id,
                phone_id: xmppData.conn.phone_id,
                username: xmppData.conn.username,
                host: xmppData.conn.host,
                muc_host: xmppData.conn.muc_host,
                sid: xmppData.conn.sid,
                rid: xmppData.conn.rid,
                jid: xmppData.conn.jid,
                http_bind_url: xmppData.http_bind_url,
                ws_bind_url: xmppData.ws_bind_url
            });
        }else{
            xmpp.getAuthData();
        }
        startCheckConnection();
    };

    xmpp.getAuthData = function(call_back){
        $http.post('/api/auth/xmpp_reconnect/').
        success(function(data, status, headers, config){
            var r = data;
            if(r.success){
                var xmppData = r.response;
                xmpp.updateScope({
                    phone_id: xmppData.conn.phone_id,
                    user_id: xmppData.conn.user_id,
                    username: xmppData.conn.username,
                    host: xmppData.conn.host,
                    muc_host: xmppData.conn.muc_host,
                    sid: xmppData.conn.sid,
                    rid: xmppData.conn.rid,
                    jid: xmppData.conn.jid,
                    http_bind_url: xmppData.http_bind_url,
                    ws_bind_url: xmppData.ws_bind_url
                });
                console.log(xmppData.conn.sid, '====================')
                console.log(xmppData);
            }
            if(_.isFunction(call_back)){
                call_back(r);
            }
        }).
        error(function(data, status, headers, config){
            // TODO: direct go to login page
            console.log(r);
        })
    };

    xmpp.genHashPasswd = function(sid, rid, jid){
        if(!sid || !rid || !jid){
            var sid = xmpp.scope.sid,
                rid = xmpp.scope.rid,
                jid = xmpp.scope.jid;
        }
        var hash = JSJaC.hex_sha1(sid+rid+jid);
        return hash;
    };


    xmpp.connect = function(){
        console.log('connect start..........');

        // if(!conn && "WebSocket" in window){
        //     conn = new jsjac.JSJaCWebSocketConnection({
        //         httpbase : xmpp.scope.ws_bind_url,
        //         oDbg : new jsjac.JSJaCConsoleLogger(1)
        //     });
        // }

        if(!conn){
            conn = new jsjac.JSJaCHttpBindingConnection({
                httpbase : xmpp.scope.http_bind_url,
                oDbg : new jsjac.JSJaCConsoleLogger(1)
            });
        }
        setupCon(conn);
        conn.connect({
            domain: xmpp.scope.jid.split('@')[1],//scope.get('host'),
            username: xmpp.scope.jid.split('@')[0],//scope.get('user_id'),
            resource: xmpp.scope.resource,
            pass: xmpp.genHashPasswd(),
            register: false
        });
    };

    xmpp.disconnect = function(logout){
        xmpp.scope.connecting = false;
        var p = new jsjac.JSJaCPresence();
        p.setType("unavailable");
        var join_rooms = xmpp.scope.join_rooms;
        for(var roomid in join_rooms){
            join_rooms[roomid] = 'discoonected'
        }
        if(conn){
            conn.send(p);
            conn.disconnect();
            unregisterCon(conn);
        }
        if(logout){
            stopCheckConnection();
            xmpp.initScope();
        }else{
            xmpp.reconnect();
        }
        xmpp.scope.$broadcast('disconnect');
    };

    xmpp.reconnect = function(){
        xmpp.getAuthData();
        xmpp.scope.reconnect = true;
        xmpp.scope.connecting = false;
    };

    xmpp.joinMuc = function(roomJID){
        console.log(roomJID)
        if(!roomJID){
            return false;
        }
        if(xmpp.scope.join_rooms[roomJID] == 'connected'){
            return true;
        }
        if(xmpp.scope[roomJID] == undefined){
            xmpp.scope[roomJID] = 0;
        }else{
            xmpp.scope[roomJID]++;
            xmpp.scope.$apply();
        }
        if(xmpp.scope.connected){
            var joinPacket = new jsjac.JSJaCPresence();
            joinPacket.setTo(roomJID+'/'+xmpp.scope.user_id+'-'+xmpp.scope.resource);
            joinPacket.setFrom(xmpp.scope.jid+'/'+xmpp.scope.resource);
            joinPacket.setID(xmpp.getUniqueId()+'_joinMuc');

            conn.send(joinPacket);
            xmpp.scope[roomJID] = undefined
        }else{
            setTimeout(function(){
                if(xmpp.scope[roomJID] < 5){
                    console.log('reconnect muc: '+roomJID);
                    xmpp.joinMuc(roomJID)    
                }else{
                    if(xmpp.scope.logout==false){
                        xmpp.discoonect();
                    }
                }
            }, 1000);
        }
    };

    xmpp.leaveMuc = function(roomJID){
        if(!roomJID){
            return false;
        }
        var leavePacket = new jsjac.JSJaCPresence();
        leavePacket.setTo(roomJID+'/'+xmpp.scope.user_id+'-'+xmpp.scope.resource);
        leavePacket.setFrom(xmpp.scope.jid+'/'+xmpp.scope.resource);
        leavePacket.setType("unavailable");

        conn.send(leavePacket);
        delete xmpp.scope.join_rooms[roomJID];
    };

    xmpp.reJoinRooms = function(){
        var join_rooms = xmpp.scope.join_rooms;
        for(var roomid in join_rooms){
            if(roomid.split('@')[0].match(/-pubsub/))
                continue;
            if(join_rooms[roomid] == 'discoonected'){
                xmpp.joinMuc(roomid);
            }
        }
    };

    xmpp.sendMsg = function(roomJID, msgContent, msgUuid, displayName, combine, combinebody){
        if(msgContent == '')
            return false;

        var oMsg = new jsjac.JSJaCMessage();
        oMsg.setTo(roomJID);
        oMsg.setBody(msgContent);
        oMsg.setType("groupchat");
        var info = oMsg.getDoc().createElement('info');
        var node = oMsg.getNode();

        info.setAttribute('xmlns', 'extra:attrs');

        node.setAttribute('display_name', displayName);
        node.setAttribute('msguuid', msgUuid);
        node.setAttribute('userid', xmpp.scope.user_id || '');
        node.setAttribute('phoneid', xmpp.scope.phone_id || '');

        info.setAttribute('display_name', displayName);
        info.setAttribute('msguuid', msgUuid);
        info.setAttribute('userid', xmpp.scope.user_id || '');
        info.setAttribute('phoneid', xmpp.scope.phone_id || '');

        if(combine){
            node.setAttribute('combine', combine);
            node.setAttribute('combinebody', combinebody);
            info.setAttribute('combine', combine);
            info.setAttribute('combinebody', combinebody);
        }else{
            node.setAttribute('combine', '');
            node.setAttribute('combinebody', '');
            info.setAttribute('combine', '');
            info.setAttribute('combinebody', '');
        }

        node.appendChild(info);

        // console.log(oMsg.xml());

        try{
            conn.send(oMsg);
            xmpp.scope.$broadcast("msg:send", [msgUuid]);
        }catch(e){
            console.error('Could not send the message: ', e.message);
            xmpp.scope.$broadcast("msg:send:error", [msgUuid]);
        }

        return true;
    };

    xmpp.buildMsgObject = function(oJSJaCPacket){

        var fromJID = oJSJaCPacket.getFromJID();
        var toJID = oJSJaCPacket.getToJID();
        var body = oJSJaCPacket.getBody();//.htmlEnc();
        var timestamp = new Date().getTime();
        var userid = oJSJaCPacket._getAttribute('userid')
        var msguuid = oJSJaCPacket._getAttribute('msguuid');
        var display_name = oJSJaCPacket._getAttribute('display_name');
        var phoneid = oJSJaCPacket._getAttribute('phoneid');
        var combine = oJSJaCPacket._getAttribute('combine');
        var combinebody = oJSJaCPacket._getAttribute('combinebody');

        return {
            id: msguuid,
            msg_uuid: msguuid,
            content: body,
            from_user: {
                id: userid//,
                // username: toJID.getNode(),
            },
            from_display_name: display_name,
            from_jid: fromJID.getBareJID(),
            from_host: fromJID.getDomain(),
            from_resource: fromJID.getResource(),
            to_jid: toJID.getBareJID(),
            to_host: toJID.getDomain(),
            to_resource: toJID.getResource(),
            read_users: [],
            timestamp: timestamp,
            timestamp_micro: timestamp*1000,
            combine: combine,
            phoneid: phoneid,
            combinebody: combinebody
        }
    };

    xmpp.ping = function(){
        pingTimer = setTimeout(checkPong, 5000);
        var iq = new jsjac.JSJaCIQ();
        var ping_id = xmpp.getUniqueId()+'_ping';
        n = iq.getNode();
        n.setAttribute('type', 'get');
        n.setAttribute('id', ping_id);
        var ping = iq.buildNode('ping');
        ping.setAttribute('xmlns', jsjac.NS_PING);
        iq.appendNode(ping);

        xmpp.scope.last_ping = ping_id;
        xmpp.scope.$apply();

        conn.send(iq);
    };

    function startCheckConnection(){
        checkConnTimer = setInterval(xmpp.ping, 10000);
    };

    function stopCheckConnection(){
        clearInterval(checkConnTimer);
        checkConnTimer = null;
    };

    function checkPong(){
        if(xmpp.scope.last_ping != true){
            xmpp.pongtimes = xmpp.pongtimes || 0;
            xmpp.pongtimes++;
            console.log('checkpong')
            // xmpp.reconnect();
            if((!xmpp.scope.getconnected && !xmpp.scope.connected) || xmpp.pongtimes>3){
                xmpp.disconnect();
            }
        }else{
            clearTimeout(pingTimer);
            pingTimer = null;
            xmpp.pongtimes = 0;
        }
    };

    function handleRoomJoin(oJSJaCPacket) {
        var item = _getItemChild(oJSJaCPacket);
        if(!item){
            console.log('room join error...');
            return false;
        }
        var roomJID = oJSJaCPacket.getFromJID().getBareJID();
        xmpp.scope.join_rooms[roomJID] = 'connecting';
        xmpp.scope.$apply();
    };

    function displayPresence(oJSJaCPacket){
        // console.log('== displayPresence', oJSJaCPacket.doc);
    };

    function handleIQ(oIQ){
        // console.log('==:handleIQ:',oIQ, oIQ.xml());
        if(xmpp.scope.last_ping == oIQ.getID()){
            // pong
            xmpp.scope.last_ping = true;
            xmpp.scope.$apply();
            clearTimeout(pingTimer);
            pingTimer = null;
        }else{

        }     
    };

    function handleMessage(oJSJaCPacket){
        console.log(oJSJaCPacket.xml());
        var fromJID = oJSJaCPacket.getFromJID();
        var toJID = oJSJaCPacket.getToJID();
        var body = oJSJaCPacket.getBody().htmlEnc();
        var node = oJSJaCPacket.getNode();
        // console.log('----------',oJSJaCPacket.xml(),'-----------')

        if(toJID.getBareJID().toString() == xmpp.scope.jid){
            if(body == ''){
                if(xmpp.scope.join_rooms[fromJID.getBareJID()]){
                    xmpp.scope.join_rooms[fromJID.getBareJID()] = 'connected';
                    xmpp.scope.$apply();
                    if(xmpp.scope.reconnect){
                        xmpp.scope.$broadcast(fromJID.getBareJID()+":muc:rejoin:success");
                    }else{
                        xmpp.scope.$broadcast(fromJID.getBareJID()+":muc:join:success");
                    }
                }
            }else{
                if(node.getAttribute('type') == 'pubsub'){
                    try{
                        var pubsub_json = JSON.parse(oJSJaCPacket.getBody());
                        var action_type = pubsub_json.action_type;

                        console.log(action_type);
                        if(action_type){
                            /*
                                /chat/msg/receive
                                /chat/msg/read
                                /profile/email/verify
                            */
                            xmpp.scope.$broadcast(action_type, [pubsub_json]);
                        }else{
                            xmpp.scope.$broadcast("pubsub:receive", [pubsub_json]);
                        }
                    }catch(e){console.log(e.message,'pubsub error=======');}
                }else{
                    xmpp.scope.$broadcast(fromJID.getBareJID().toString()+":msg:receive", [xmpp.buildMsgObject(oJSJaCPacket)]);
                }
            }
        }
    };

    function handlePresence(oJSJaCPacket){
        console.log('==:handlePresence:',oJSJaCPacket.xml());
        console.log('==:getResource:',oJSJaCPacket.getFromJID().getResource());
        if(oJSJaCPacket.getFromJID().getResource() == xmpp.scope.user_id) {
            handleRoomJoin(oJSJaCPacket);
        } else {
            displayPresence(oJSJaCPacket);
        }
    };

    function handleError(oJSJaCPacket){
        console.log('==:handleError:',oJSJaCPacket);
        // xmpp.reconnect();
        xmpp.disconnect();
    };

    function handleStatusChanged(oJSJaCPacket){
        // console.log('==:handleStatusChanged:',oJSJaCPacket);
    };

    function handleConnected(oJSJaCPacket){
        // console.log('==:handleConnected:',oJSJaCPacket);
        xmpp.scope.connected = true;
        xmpp.scope.connecting = false;
        xmpp.scope.$broadcast('connected');
        conn.send(new jsjac.JSJaCPresence(), function(){
            console.log('just send presence..');
            xmpp.onConnected(xmpp.scope);
            // startCheckConnection();
            xmpp.reJoinRooms();
            if(xmpp.scope.reconnect){
                xmpp.scope.$broadcast('reconnected');
            }
            xmpp.scope.reconnect = false;
        });
        // console.log('==:handleConnected:',oJSJaCPacket);
    };

    function handleDisconnected(oJSJaCPacket){
        xmpp.scope.connected = false;
        xmpp.scope.connecting = false;
        xmpp.scope.reconnect = false;
        clearTimeout(pingTimer);
        pingTimer = null;
        console.log('----------------------------- discoonected');
    };

    function setupCon(oCon){
        oCon.registerHandler('message', handleMessage);
        oCon.registerHandler('presence', handlePresence);
        oCon.registerHandler('iq', handleIQ);
        oCon.registerHandler('onconnect', handleConnected);
        oCon.registerHandler('onerror', handleError);
        oCon.registerHandler('status_changed', handleStatusChanged);
        oCon.registerHandler('ondisconnect', handleDisconnected);
    };

    function unregisterCon(oCon){
        oCon.unregisterHandler('message', handleMessage);
        oCon.unregisterHandler('presence', handlePresence);
        oCon.unregisterHandler('iq', handleIQ);
        oCon.unregisterHandler('onconnect', handleConnected);
        oCon.unregisterHandler('onerror', handleError);
        oCon.unregisterHandler('status_changed', handleStatusChanged);
        oCon.unregisterHandler('ondisconnect', handleDisconnected);
    }

    function _getItemChild(presence) {
        var nodes = presence.getChild("x").childNodes;
        for(var i in nodes) {
            if(nodes[i].nodeName == "item")
            return nodes[i];
        }
        return false;
    }

    xmpp.initScope();
}]);