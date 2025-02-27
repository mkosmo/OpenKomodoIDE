/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
'use strict';
var { Buffer } = require("contrib/buffer");
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var events_1 = require("./events");
var Is = require("./is");
var ContentLength = 'Content-Length: ';
var CRLF = '\r\n';
var MessageWriter;
(function (MessageWriter) {
    function is(value) {
        var candidate = value;
        return candidate && Is.func(candidate.dispose) && Is.func(candidate.onClose) &&
            Is.func(candidate.onError) && Is.func(candidate.write);
    }
    MessageWriter.is = is;
})(MessageWriter = exports.MessageWriter || (exports.MessageWriter = {}));
var AbstractMessageWriter = /** @class */ (function () {
    function AbstractMessageWriter() {
        this.errorEmitter = new events_1.Emitter();
        this.closeEmitter = new events_1.Emitter();
    }
    AbstractMessageWriter.prototype.dispose = function () {
        this.errorEmitter.dispose();
        this.closeEmitter.dispose();
    };
    Object.defineProperty(AbstractMessageWriter.prototype, "onError", {
        get: function () {
            return this.errorEmitter.event;
        },
        enumerable: true,
        configurable: true
    });
    AbstractMessageWriter.prototype.fireError = function (error, message, count) {
        this.errorEmitter.fire([this.asError(error), message, count]);
    };
    Object.defineProperty(AbstractMessageWriter.prototype, "onClose", {
        get: function () {
            return this.closeEmitter.event;
        },
        enumerable: true,
        configurable: true
    });
    AbstractMessageWriter.prototype.fireClose = function () {
        this.closeEmitter.fire(undefined);
    };
    AbstractMessageWriter.prototype.asError = function (error) {
        if (error instanceof Error) {
            return error;
        }
        else {
            return new Error("Writer recevied error. Reason: " + (Is.string(error.message) ? error.message : 'unknown'));
        }
    };
    return AbstractMessageWriter;
}());
exports.AbstractMessageWriter = AbstractMessageWriter;
var StreamMessageWriter = /** @class */ (function (_super) {
    __extends(StreamMessageWriter, _super);
    function StreamMessageWriter(writable, encoding) {
        if (encoding === void 0) { encoding = 'utf8'; }
        var _this = _super.call(this) || this;
        _this.writable = writable;
        _this.encoding = encoding;
        _this.errorCount = 0;
        _this.writable.on('error', function (error) { return _this.fireError(error); });
        _this.writable.on('close', function () { return _this.fireClose(); });
        return _this;
    }
    StreamMessageWriter.prototype.write = function (msg) {
        var json = JSON.stringify(msg);
        var contentLength = Buffer.byteLength(json, this.encoding);
        var headers = [
            ContentLength, contentLength.toString(), CRLF,
            CRLF
        ];
        try {
            // Header must be written in ASCII encoding
            this.writable.write(headers.join(''), 'ascii');
            // Now write the content. This can be written in any encoding
            this.writable.write(json, this.encoding);
            this.errorCount = 0;
        }
        catch (error) {
            this.errorCount++;
            this.fireError(error, msg, this.errorCount);
        }
    };
    return StreamMessageWriter;
}(AbstractMessageWriter));
exports.StreamMessageWriter = StreamMessageWriter;
var IPCMessageWriter = /** @class */ (function (_super) {
    __extends(IPCMessageWriter, _super);
    function IPCMessageWriter(process) {
        var _this = _super.call(this) || this;
        _this.process = process;
        _this.errorCount = 0;
        _this.queue = [];
        _this.sending = false;
        var eventEmitter = _this.process;
        eventEmitter.on('error', function (error) { return _this.fireError(error); });
        eventEmitter.on('close', function () { return _this.fireClose; });
        return _this;
    }
    IPCMessageWriter.prototype.write = function (msg) {
        if (!this.sending && this.queue.length === 0) {
            // See https://github.com/nodejs/node/issues/7657
            this.doWriteMessage(msg);
        }
        else {
            this.queue.push(msg);
        }
    };
    IPCMessageWriter.prototype.doWriteMessage = function (msg) {
        var _this = this;
        try {
            if (this.process.send) {
                this.sending = true;
                this.process.send(msg, undefined, undefined, function (error) {
                    _this.sending = false;
                    if (error) {
                        _this.errorCount++;
                        _this.fireError(error, msg, _this.errorCount);
                    }
                    else {
                        _this.errorCount = 0;
                    }
                    if (_this.queue.length > 0) {
                        _this.doWriteMessage(_this.queue.shift());
                    }
                });
            }
        }
        catch (error) {
            this.errorCount++;
            this.fireError(error, msg, this.errorCount);
        }
    };
    return IPCMessageWriter;
}(AbstractMessageWriter));
exports.IPCMessageWriter = IPCMessageWriter;
var SocketMessageWriter = /** @class */ (function (_super) {
    __extends(SocketMessageWriter, _super);
    function SocketMessageWriter(socket, encoding) {
        if (encoding === void 0) { encoding = 'utf8'; }
        var _this = _super.call(this) || this;
        _this.socket = socket;
        _this.queue = [];
        _this.sending = false;
        _this.encoding = encoding;
        _this.errorCount = 0;
        _this.socket.on('error', function (error) { return _this.fireError(error); });
        _this.socket.on('close', function () { return _this.fireClose(); });
        return _this;
    }
    SocketMessageWriter.prototype.write = function (msg) {
        if (!this.sending && this.queue.length === 0) {
            // See https://github.com/nodejs/node/issues/7657
            this.doWriteMessage(msg);
        }
        else {
            this.queue.push(msg);
        }
    };
    SocketMessageWriter.prototype.doWriteMessage = function (msg) {
        var _this = this;
        var json = JSON.stringify(msg);
        var contentLength = Buffer.byteLength(json, this.encoding);
        var headers = [
            ContentLength, contentLength.toString(), CRLF,
            CRLF
        ];
        try {
            // Header must be written in ASCII encoding
            this.sending = true;
            this.socket.write(headers.join(''), 'ascii', function (error) {
                if (error) {
                    _this.handleError(error, msg);
                }
                try {
                    // Now write the content. This can be written in any encoding
                    _this.socket.write(json, _this.encoding, function (error) {
                        _this.sending = false;
                        if (error) {
                            _this.handleError(error, msg);
                        }
                        else {
                            _this.errorCount = 0;
                        }
                        if (_this.queue.length > 0) {
                            _this.doWriteMessage(_this.queue.shift());
                        }
                    });
                }
                catch (error) {
                    _this.handleError(error, msg);
                }
            });
        }
        catch (error) {
            this.handleError(error, msg);
        }
    };
    SocketMessageWriter.prototype.handleError = function (error, msg) {
        this.errorCount++;
        this.fireError(error, msg, this.errorCount);
    };
    return SocketMessageWriter;
}(AbstractMessageWriter));
exports.SocketMessageWriter = SocketMessageWriter;
