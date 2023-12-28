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

#define COMMAND_SETTER_BOILERPLATE "\n\n  Not all headers are processed by AMPS for all commands. See the AMPS Command Reference for which headers are used by AMPS for a specific command.\n\n  :param value: The new value to set for the header\n\n  :returns: this command"


static const char* command_class_doc = "\n"
                                       "  AMPS.Command represents a single message (or *command*) sent to the"
                                       "  AMPS server. The class provides methods for headers that are used"
                                       "  for commands to the server. Applications typically use this class"
                                       "  to create outgoing requests to AMPS. The responses to requests,"
                                       "  whether acknowledgements or messages that contain data, are"
                                       "  returned as instances of the :class:`AMPS.Message` class.\n\n"
                                       "  The :class:`AMPS.Client` provides named convenience methods that support"
                                       "  a subset of the options available via a Command. For most applications,"
                                       "  the recommended approach is to use the ``publish()`` methods for sending"
                                       "  data to AMPS (unless the application needs to set options not"
                                       "  available through that method) and use the Command class for queries,"
                                       "  subscriptions, and to remove data.\n\n"
                                       "  To use the Command class to run a command on the server, you create the"
                                       "  Command, set options as described in the Command Cookbook in the"
                                       "  Python Developer Guide or the AMPS Command Reference, and then use"
                                       "  :func:`AMPS.Client.execute_async()` to process messages asynchronously,"
                                       "  or :func:`AMPS.Client.execute()` to process messages synchronously.\n\n"
                                       ;
static const char* reset_doc = "\n"
                               "  Resets this command with a new Command type and re-initializes all other fields.\n\n"
                               ":param: A string indicating the AMPS command.\n";
static const char* set_sow_key_doc = "\n"
                                     "  Sets the SOW key for this command. This is useful for ``publish``\n"
                                     "  commands.\n\n"
                                     "  For a ``publish`` command, sets the SOW key for a message when the SOW\n"
                                     "  is configured so that the publisher is responsible for determining and\n"
                                     "  providing the SOW key. This option is ignored on a ``publish`` when\n"
                                     "  the topic is configured with a ``Key`` field in the SOW file.\n\n"
                                     COMMAND_SETTER_BOILERPLATE;
static const char* set_sow_keys_doc = "\n"
                                      "  The sow keys for a command are a comma-separated list\n"
                                      "  of the keys that AMPS assigns to SOW messages. The SOW key for a\n"
                                      "  message is available through the ``Message.get_sow_key()`` method on a message.\n\n"
                                      "  For a ``sow_delete`` command, this list indicates the set of messages to\n"
                                      "  be deleted.\n\n"
                                      "  For a query or subscription, this list indicates the set of messages to\n"
                                      "  include in the query or subscription.\n\n"
                                      COMMAND_SETTER_BOILERPLATE;

static const char* set_command_id_doc = "\n"
                                        "  Sets the value of the *command id* header. This header is used to "
                                        "  identify responses to the command. The AMPS FAQ has details on the relationship between command ID, subscription ID, and query ID.\n\n"
                                        "  If not set, the AMPS Client will automatically fill in a *command id* "
                                        "  when the client needs one to be present (for example, when the client "
                                        "  needs a ``processed`` acknowledgement to be able to tell if a "
                                        "  ``subscribe`` command succeeded or failed).\n\n"
                                        "  :param value: the new value for this header\n\n"
                                        "  :returns: this command\n\n";

static const char* set_topic_doc = "\n"
                                   "  Sets the value of the *topic* header, which specifies the topic that"
                                   "  the command applies to. For a ``publish`` command, this field is"
                                   "  interpreted as the literal topic to publish to. For commands such as"
                                   "  ``sow`` or ``subscribe``, the topic is interpreted as a literal topic"
                                   "  unless there are regular expression characters present in the topic"
                                   "  name. For those commands, if regular expression characters are present,"
                                   "  the command will be interpreted as applying to all topics with names"
                                   " that match the regular expression.\n\n"
                                   COMMAND_SETTER_BOILERPLATE;

static const char* set_filter_doc = "\n"
                                    " Sets the value of the filter header.\n\n"
                                    COMMAND_SETTER_BOILERPLATE;

static const char* set_order_by_doc = "\n"
                                      "  Sets the value of the order by header. This header is only used for SOW"
                                      "  query results, and must contain one or more XPath identifiers"
                                      "  and an optional ``ASC`` or ``DESC`` order specifier (for example,"
                                      "  ``/orderTimestamp DESC``).\n\n"
                                      COMMAND_SETTER_BOILERPLATE;

static const char* set_sub_id_doc = "\n"
                                    "  Sets the subscription id of self.\n\n"
                                    COMMAND_SETTER_BOILERPLATE;

static const char* set_query_id_doc = "\n"
                                      "  Sets the query id of self.\n\n"
                                      COMMAND_SETTER_BOILERPLATE;

static const char* set_bookmark_doc = "\n"
                                      "  Sets the value of the bookmark header. For a subscription,"
                                      "  this identifies the point in the transaction log at which to begin the"
                                      "  replay. For a sow delete (queue acknowledgement), this indicates the"
                                      "  message or messages to acknowledge. For a query on a SOW topic with"
                                      "  History configured, this indicates the point at which to query"
                                      "  the topic.\n\n"
                                      COMMAND_SETTER_BOILERPLATE;

static const char* set_correlation_id_doc = "\n"
                                            "  Sets the value of the correlation ID header."
                                            "  The AMPS server does not process or interpret this value; however, the"
                                            "  value must contain only characters that are valid in Base64 encoding for"
                                            "  the server to be guaranteed to process the Command.\n\n"
                                            COMMAND_SETTER_BOILERPLATE;

static const char* set_options_doc = "\n"
                                     "  Sets the value of the options header. The options available, and how "
                                     "  AMPS interprets the options, depend on the command being sent. The "
                                     "  :class:`AMPS.Message.Options` class contains constants and helper "
                                     "  methods for building an options string. See the "
                                     "  AMPS Command Reference for details on the options available for "
                                     "  a given command.\n\n"
                                     "  :param value: The value to set\n\n"
                                     "  :returns: this command\n\n"
                                     ;

static const char* add_ack_type_doc = "\n"
                                      "  Adds an ack type to this command, in addition to any other ack types"
                                      "  that have been previously set or that will be set by the Client.\n\n"
                                      "  :param value: The ack type to add\n\n"
                                      "  :returns: this command";

static const char* set_ack_type_doc = "\n"
                                      "  Sets the ack type for this command, replacing any other ack types"
                                      "  that have been previously set or that will be set by the Client.\n\n"
                                      "  :param value: The ack type to set\n\n"
                                      "  :returns: this command";

static const char* set_ack_type_enum_doc = "\n"
                                           "  Sets the ack type enum for this command, replacing any other ack types"
                                           "  that have been previously set or that will be set by the Client.\n\n"
                                           "  :param value: The ack type to set\n\n"
                                           "  :returns: this command";

static const char* get_ack_type_doc = "\n"
                                      "  Gets the ack type enum for this command\n\n"
                                      "  :returns: the ack type as a string";

static const char* get_ack_type_enum_doc = "\n"
                                           "  Gets the ack type enum for this command\n\n"
                                           "  :returns: the ack type as an enum";

static const char* set_data_doc = "\n"
                                  "  Sets the data for this command. This is used for ``publish``"
                                  "  commands and for ``sow_delete`` commands.\n\n"
                                  COMMAND_SETTER_BOILERPLATE;

static const char* set_timeout_doc = "\n"
                                     "  Sets the amount of time that the Client will wait for a ``processed``"
                                     "  acknowledgement from the server to be received and consumed before"
                                     "  abandoning the request; this option is *only* used by the Client and"
                                     "  is not sent to the server. The acknowledgement is processed on the"
                                     "  client receive thread,"
                                     "  This option is expressed in milliseconds, where a value of ``0`` means"
                                     "  to wait indefinitely.\n\n"
                                     "  :param value: the value to set\n\n"
                                     "  :returns: this command\n\n"
                                     ;

static const char* set_top_n_doc = "\n"
                                   "  Sets the top N header of this command. Although AMPS accepts a top N"
                                   "  value in the header of a command, most AMPS applications pass the value"
                                   "  in the ``top_n`` option for clarity.\n\n"
                                   COMMAND_SETTER_BOILERPLATE;

static const char* set_batch_size_doc =
  "\n  Sets the batch size header, which is used to control the number of records that AMPS will send in each batch when returning the results of a SOW query. See the AMPS User Guide for details on SOW query batches.\n\n"
  COMMAND_SETTER_BOILERPLATE;
static const char* set_expiration_doc = "\n  Sets the expiration of self. For a publish to a SOW topic or queue, this sets the number of seconds the message will be active before expiring.\n\n"
                                        COMMAND_SETTER_BOILERPLATE;
static const char* set_sequence_doc = "\n  Sets the sequence of self for publish, delta_publish, or sow_delete commands. A publish store on the client may replace this value.\n\n"
                                      COMMAND_SETTER_BOILERPLATE;
static const char* get_sequence_doc =
  "\n  Gets the sequence of self for publish, delta_publish, or sow_delete commands. This can be checked after calling execute or executeAsync to query the sequence number that was used, if any.\n\n";

