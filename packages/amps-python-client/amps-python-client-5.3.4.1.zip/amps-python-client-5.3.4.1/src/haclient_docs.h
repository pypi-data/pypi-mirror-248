////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2010-2023 60East Technologies Inc., All Rights Reserved.
//
// This computer software is owned by 60East Technologies Inc. and is
// protected by U.S. copyright laws and other laws and by international
// treaties.  This computer software is furnished by 60East Technologies
// Inc. pursuant to a written license agreement and may be used, copied,
// transmitted, and stored only in accordance with the terms of such
// license agreement and with the inclusion of the above copyright notice.
// This computer software or any other copies thereof may not be provided
// or otherwise made available to any other person.
//
// U.S. Government Restricted Rights.  This computer software: (a) was
// developed at private expense and is in all respects the proprietary
// information of 60East Technologies Inc.; (b) was not developed with
// government funds; (c) is a trade secret of 60East Technologies Inc.
// for all purposes of the Freedom of Information Act; and (d) is a
// commercial item and thus, pursuant to Section 12.212 of the Federal
// Acquisition Regulations (FAR) and DFAR Supplement Section 227.7202,
// Government's use, duplication or disclosure of the computer software
// is subject to the restrictions set forth by 60East Technologies Inc..
//
////////////////////////////////////////////////////////////////////////////

static const char* class_doc = "AMPS HAClient Object used for highly-available client connections. Derives from :class:`Client`. Constructor arguments:\n\n"
                               ":param name: the unique name for this client. AMPS does not enforce "
                               " specific restrictions on the character set used, however some protocols"
                               " (for example, XML) may not allow specific characters. 60East recommends"
                               " that the client name be meaningful, short, human readable, and avoid"
                               " using control characters, newline characters, or square brackets.\n"
                               ":param publish_store: an optional file name for the client's local publish store. If not supplied a memory-backed publish store is used.\n"
                               ":param bookmark_store: an optional file name for the client's local bookmark store. If not supplied a memory-backed bookmark store is used.\n"
                               ":param no_store: pass no_store=True to indicate that a memory bookmark and/or publish store should not be used.\n";

static const char* connect_and_logon_doc =
  "Connects and logs on using the ServerChooser you've supplied via :meth:`set_server_chooser`. Will continue attempting to connect and logon to each URI returned by the ServerChooser until the connection succeeds or the ServerChooser returns an empty URI.";

static const char* haclient_connect_doc = "Not used in the HAClient; call :meth:`connect_and_logon` to connect and log on to AMPS once a server chooser is set.";

static const char* discard_doc = "discard(message)\n\n"
                                 "Discards a message from the local bookmark store.\n"
                                 "\n"
                                 ":param message: an AMPS.Message instance that was received from a bookmark subscription.\n"
                                 ":type message: AMPS.Message\n";

static const char* prune_store_doc = "prune_store(tmp_file_name)\n\n"
                                     "Prunes the local bookmark store. If it's file-based, it will remove unnecessary entries from the file.\n"
                                     "\n"
                                     ":param tmp_file_name: Optional file name to use for temporary storage during prune operation.\n"
                                     ":type tmp_file_name: string\n";

static const char* get_most_recent_doc = "get_most_recent(sub_id)\n\n"
                                         "Gets the most recent bookmark from the local bookmark store for the given subscription id.\n"
                                         "\n"
                                         ":param sub_id: The subscription id for which to retrieve the most recent bookmark.\n"
                                         ":type sub_id: string\n";


static const char* set_server_chooser_doc = "set_server_chooser(serverChooser)\n\n"
                                            "Sets a server chooser on self.\n"
                                            "\n"
                                            ":param serverChooser: a ServerChooser instance, such as a :class:`DefaultServerChooser`.\n"
                                            ":type serverChooser: ServerChooser\n";

static const char* get_server_chooser_doc = "get_server_chooser()\n\n"
                                            "Gets selfs server chooser and returns it.\n";

static const char* set_logon_options_doc = "set_logon_options(options)\n\n"
                                           "Sets a logon options on self.\n"
                                           "\n"
                                           ":param options: an options string to be passed to the server during logon, such as ack_conflation=100us.\n"
                                           ":type options: string\n";

static const char* get_logon_options_doc = "get_logon_options()\n\n"
                                           "Gets self's logon options string and returns it.\n";

static const char* set_timeout_doc = "set_timeout(timeout)\n\n"
                                     "Sets the timeout in milliseconds used when sending a logon command to the server.\n"
                                     "Default value is 10000 (10 seconds).\n"
                                     ":param timeout: The number of milliseconds to wait for a server response to logon. 0 indicates no timeout.\n";

static const char* set_reconnect_delay_doc = "set_reconnect_delay(reconnectDelay)\n\n"
                                             "Sets the delay in milliseconds used when reconnecting, after a disconnect occurs. Calling this method creates and installs a new FixedDelayStrategy in this client.\n"
                                             "Default value is 200 (0.2 seconds).\n"
                                             ":param reconnectDelay: The number of milliseconds to wait before reconnecting, after a disconnect occurs.\n";

static const char* set_reconnect_delay_strategy_doc =
  "set_reconnect_delay_strategy(reconnectDelayStrategy)\n\n"
  "Sets the reconnect delay strategy object used to control delay behavior\n"
  "when connecting and reconnecting to servers.\n\n"
  ":param strategy: The reconnect delay strategy object to use when\n"
  " connecting and reconnecting to AMPS instances. The object must have\n"
  " the following two methods defined:\n\n"
  "   get_connect_wait_duration(uri):\n"
  "     *uri* A string containing the next URI AMPS will connect with.\n"
  "     *returns*   An integer representing the time in milliseconds to wait "
  "                 before connecting to that URI.\n\n\n"
  "   reset(): resets the state of self after a successful connection.\n\n";

static const char* get_reconnect_delay_strategy_doc =
  "get_reconnect_delay_strategy()\n\n"
  "Returns the reconnect delay strategy object used to control delay behavior\n"
  "when connecting and reconnecting to servers.\n\n"
  ":returns: The reconnect delay strategy object.";

static const char* get_default_resubscription_timeout_doc = "get_default_resubscription_timeout()\n\n"
                                                            "Gets the default timeout in milliseconds used when attempting to resubscribe\n"
                                                            "each subscription after a re-connect.\n";

static const char* set_default_resubscription_timeout_doc = "set_default_resubscription_timeout(timeout)\n\n"
                                                            "Sets the default timeout in milliseconds used when attempting to resubscribe\n"
                                                            "each subscription after a re-connect. Default value is 0 (no timeout).\n"
                                                            ":param timeout: The number of milliseconds to wait for a server response. 0 indicates no timeout.\n";

static const char* get_resubscription_timeout_doc = "get_resubscription_timeout()\n\n"
                                                    "Gets the timeout in milliseconds used when attempting to resubscribe each\n"
                                                    "subscription after a re-connect.\n";

static const char* set_resubscription_timeout_doc = "set_resubscription_timeout(timeout)\n\n"
                                                    "Sets the timeout in milliseconds used when attempting to resubscribe each\n"
                                                    "subscription after a re-connect. Default value is 0 (no timeout) but can be\n"
                                                    "changed using set_default_resubscription_timeout.\n"
                                                    ":param timeout: The number of milliseconds to wait for a server response. 0 indicates no timeout.\n";

static const char* set_failed_resubscribe_handler_doc = "set_failed_resubscribe_handler(handler)\n\n"
                                                    "Sets the handler that is called if a resubscribe after failover fails to complete\n"
                                                    "successfully. The subscribe Message, requested acktypes, and exception are passed\n"
                                                    "to the handler. The handler should return False to force a new attempt at connect_and_logon\n"
                                                    "or True to ignore the failure and remove the subscription from the subscription manager.\n"
                                                    ":param handler: The callable handler to invoke.\n";

