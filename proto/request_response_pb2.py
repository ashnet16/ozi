# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: request_response.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'request_response.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import message_pb2 as message__pb2
import onchain_event_pb2 as onchain__event__pb2
import hub_event_pb2 as hub__event__pb2
import username_proof_pb2 as username__proof__pb2
import gossip_pb2 as gossip__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16request_response.proto\x1a\rmessage.proto\x1a\x13onchain_event.proto\x1a\x0fhub_event.proto\x1a\x14username_proof.proto\x1a\x0cgossip.proto\"\x07\n\x05\x45mpty\"\xae\x01\n\x10SubscribeRequest\x12\"\n\x0b\x65vent_types\x18\x01 \x03(\x0e\x32\r.HubEventType\x12\x14\n\x07\x66rom_id\x18\x02 \x01(\x04H\x00\x88\x01\x01\x12\x19\n\x0ctotal_shards\x18\x03 \x01(\x04H\x01\x88\x01\x01\x12\x18\n\x0bshard_index\x18\x04 \x01(\x04H\x02\x88\x01\x01\x42\n\n\x08_from_idB\x0f\n\r_total_shardsB\x0e\n\x0c_shard_index\"\x1a\n\x0c\x45ventRequest\x12\n\n\x02id\x18\x01 \x01(\x04\"\"\n\x0eHubInfoRequest\x12\x10\n\x08\x64\x62_stats\x18\x01 \x01(\x08\"\xa1\x01\n\x0fHubInfoResponse\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x12\n\nis_syncing\x18\x02 \x01(\x08\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x11\n\troot_hash\x18\x04 \x01(\t\x12\x1a\n\x08\x64\x62_stats\x18\x05 \x01(\x0b\x32\x08.DbStats\x12\x0e\n\x06peerId\x18\x06 \x01(\t\x12\x18\n\x10hub_operator_fid\x18\x07 \x01(\x04\"f\n\x07\x44\x62Stats\x12\x14\n\x0cnum_messages\x18\x01 \x01(\x04\x12\x16\n\x0enum_fid_events\x18\x02 \x01(\x04\x12\x18\n\x10num_fname_events\x18\x03 \x01(\x04\x12\x13\n\x0b\x61pprox_size\x18\x04 \x01(\x04\"3\n\x11SyncStatusRequest\x12\x13\n\x06peerId\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\t\n\x07_peerId\"b\n\x12SyncStatusResponse\x12\x12\n\nis_syncing\x18\x01 \x01(\x08\x12 \n\x0bsync_status\x18\x02 \x03(\x0b\x32\x0b.SyncStatus\x12\x16\n\x0e\x65ngine_started\x18\x03 \x01(\x08\"\xc8\x01\n\nSyncStatus\x12\x0e\n\x06peerId\x18\x01 \x01(\t\x12\x0e\n\x06inSync\x18\x02 \x01(\t\x12\x12\n\nshouldSync\x18\x03 \x01(\x08\x12\x18\n\x10\x64ivergencePrefix\x18\x04 \x01(\t\x12\x1c\n\x14\x64ivergenceSecondsAgo\x18\x05 \x01(\x05\x12\x15\n\rtheirMessages\x18\x06 \x01(\x04\x12\x13\n\x0bourMessages\x18\x07 \x01(\x04\x12\x13\n\x0blastBadSync\x18\x08 \x01(\x03\x12\r\n\x05score\x18\t \x01(\x03\"{\n\x18TrieNodeMetadataResponse\x12\x0e\n\x06prefix\x18\x01 \x01(\x0c\x12\x14\n\x0cnum_messages\x18\x02 \x01(\x04\x12\x0c\n\x04hash\x18\x03 \x01(\t\x12+\n\x08\x63hildren\x18\x04 \x03(\x0b\x32\x19.TrieNodeMetadataResponse\"l\n\x18TrieNodeSnapshotResponse\x12\x0e\n\x06prefix\x18\x01 \x01(\x0c\x12\x17\n\x0f\x65xcluded_hashes\x18\x02 \x03(\t\x12\x14\n\x0cnum_messages\x18\x03 \x01(\x04\x12\x11\n\troot_hash\x18\x04 \x01(\t\" \n\x0eTrieNodePrefix\x12\x0e\n\x06prefix\x18\x01 \x01(\x0c\"\x1b\n\x07SyncIds\x12\x10\n\x08sync_ids\x18\x01 \x03(\x0c\"\x89\x01\n\nFidRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x16\n\tpage_size\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x17\n\npage_token\x18\x03 \x01(\x0cH\x01\x88\x01\x01\x12\x14\n\x07reverse\x18\x04 \x01(\x08H\x02\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"\xf4\x01\n\x13\x46idTimestampRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x16\n\tpage_size\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x17\n\npage_token\x18\x03 \x01(\x0cH\x01\x88\x01\x01\x12\x14\n\x07reverse\x18\x04 \x01(\x08H\x02\x88\x01\x01\x12\x1c\n\x0fstart_timestamp\x18\x05 \x01(\x04H\x03\x88\x01\x01\x12\x1b\n\x0estop_timestamp\x18\x06 \x01(\x04H\x04\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverseB\x12\n\x10_start_timestampB\x11\n\x0f_stop_timestamp\"}\n\x0b\x46idsRequest\x12\x16\n\tpage_size\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\npage_token\x18\x02 \x01(\x0cH\x01\x88\x01\x01\x12\x14\n\x07reverse\x18\x03 \x01(\x08H\x02\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"N\n\x0c\x46idsResponse\x12\x0c\n\x04\x66ids\x18\x01 \x03(\x04\x12\x1c\n\x0fnext_page_token\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x42\x12\n\x10_next_page_token\"`\n\x10MessagesResponse\x12\x1a\n\x08messages\x18\x01 \x03(\x0b\x32\x08.Message\x12\x1c\n\x0fnext_page_token\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x42\x12\n\x10_next_page_token\"\xc9\x01\n\x14\x43\x61stsByParentRequest\x12!\n\x0eparent_cast_id\x18\x01 \x01(\x0b\x32\x07.CastIdH\x00\x12\x14\n\nparent_url\x18\x05 \x01(\tH\x00\x12\x16\n\tpage_size\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x17\n\npage_token\x18\x03 \x01(\x0cH\x02\x88\x01\x01\x12\x14\n\x07reverse\x18\x04 \x01(\x08H\x03\x88\x01\x01\x42\x08\n\x06parentB\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"\x87\x01\n\x0fReactionRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12$\n\rreaction_type\x18\x02 \x01(\x0e\x32\r.ReactionType\x12!\n\x0etarget_cast_id\x18\x03 \x01(\x0b\x32\x07.CastIdH\x00\x12\x14\n\ntarget_url\x18\x04 \x01(\tH\x00\x42\x08\n\x06target\"\xd1\x01\n\x15ReactionsByFidRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12)\n\rreaction_type\x18\x02 \x01(\x0e\x32\r.ReactionTypeH\x00\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x17\n\npage_token\x18\x04 \x01(\x0cH\x02\x88\x01\x01\x12\x14\n\x07reverse\x18\x05 \x01(\x08H\x03\x88\x01\x01\x42\x10\n\x0e_reaction_typeB\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"\x8a\x02\n\x18ReactionsByTargetRequest\x12!\n\x0etarget_cast_id\x18\x01 \x01(\x0b\x32\x07.CastIdH\x00\x12\x14\n\ntarget_url\x18\x06 \x01(\tH\x00\x12)\n\rreaction_type\x18\x02 \x01(\x0e\x32\r.ReactionTypeH\x01\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x17\n\npage_token\x18\x04 \x01(\x0cH\x03\x88\x01\x01\x12\x14\n\x07reverse\x18\x05 \x01(\x08H\x04\x88\x01\x01\x42\x08\n\x06targetB\x10\n\x0e_reaction_typeB\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"E\n\x0fUserDataRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12%\n\x0euser_data_type\x18\x02 \x01(\x0e\x32\r.UserDataType\"(\n\x18NameRegistryEventRequest\x12\x0c\n\x04name\x18\x01 \x01(\x0c\"(\n\x19RentRegistryEventsRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\"\xb9\x01\n\x13OnChainEventRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12%\n\nevent_type\x18\x02 \x01(\x0e\x32\x11.OnChainEventType\x12\x16\n\tpage_size\x18\x03 \x01(\rH\x00\x88\x01\x01\x12\x17\n\npage_token\x18\x04 \x01(\x0cH\x01\x88\x01\x01\x12\x14\n\x07reverse\x18\x05 \x01(\x08H\x02\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"g\n\x14OnChainEventResponse\x12\x1d\n\x06\x65vents\x18\x01 \x03(\x0b\x32\r.OnChainEvent\x12\x1c\n\x0fnext_page_token\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x42\x12\n\x10_next_page_token\"p\n\x15StorageLimitsResponse\x12\x1d\n\x06limits\x18\x01 \x03(\x0b\x32\r.StorageLimit\x12\r\n\x05units\x18\x02 \x01(\r\x12)\n\x0cunit_details\x18\x03 \x03(\x0b\x32\x13.StorageUnitDetails\"L\n\x12StorageUnitDetails\x12#\n\tunit_type\x18\x01 \x01(\x0e\x32\x10.StorageUnitType\x12\x11\n\tunit_size\x18\x02 \x01(\r\"\x8a\x01\n\x0cStorageLimit\x12\x1e\n\nstore_type\x18\x01 \x01(\x0e\x32\n.StoreType\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05limit\x18\x03 \x01(\x04\x12\x0c\n\x04used\x18\x04 \x01(\x04\x12\x19\n\x11\x65\x61rliestTimestamp\x18\x05 \x01(\x04\x12\x14\n\x0c\x65\x61rliestHash\x18\x06 \x01(\x0c\"$\n\x14UsernameProofRequest\x12\x0c\n\x04name\x18\x01 \x01(\x0c\"8\n\x16UsernameProofsResponse\x12\x1e\n\x06proofs\x18\x01 \x03(\x0b\x32\x0e.UserNameProof\"3\n\x13VerificationRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0c\",\n\rSignerRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x0e\n\x06signer\x18\x02 \x01(\x0c\"M\n\x0bLinkRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x11\n\tlink_type\x18\x02 \x01(\t\x12\x14\n\ntarget_fid\x18\x03 \x01(\x04H\x00\x42\x08\n\x06target\"\xb6\x01\n\x11LinksByFidRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x16\n\tlink_type\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x17\n\npage_token\x18\x04 \x01(\x0cH\x02\x88\x01\x01\x12\x14\n\x07reverse\x18\x05 \x01(\x08H\x03\x88\x01\x01\x42\x0c\n\n_link_typeB\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"\xcc\x01\n\x14LinksByTargetRequest\x12\x14\n\ntarget_fid\x18\x01 \x01(\x04H\x00\x12\x16\n\tlink_type\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x17\n\npage_token\x18\x04 \x01(\x0cH\x03\x88\x01\x01\x12\x14\n\x07reverse\x18\x05 \x01(\x08H\x04\x88\x01\x01\x42\x08\n\x06targetB\x0c\n\n_link_typeB\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"2\n\x1fIdRegistryEventByAddressRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0c\"@\n\x13\x43ontactInfoResponse\x12)\n\x08\x63ontacts\x18\x01 \x03(\x0b\x32\x17.ContactInfoContentBody\">\n\x12ValidationResponse\x12\r\n\x05valid\x18\x01 \x01(\x08\x12\x19\n\x07message\x18\x02 \x01(\x0b\x32\x08.Message\"7\n\x19SubmitBulkMessagesRequest\x12\x1a\n\x08messages\x18\x01 \x03(\x0b\x32\x08.Message\">\n\x0cMessageError\x12\x0c\n\x04hash\x18\x01 \x01(\x0c\x12\x0f\n\x07\x65rrCode\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"f\n\x13\x42ulkMessageResponse\x12\x1b\n\x07message\x18\x01 \x01(\x0b\x32\x08.MessageH\x00\x12&\n\rmessage_error\x18\x02 \x01(\x0b\x32\r.MessageErrorH\x00\x42\n\n\x08response\"D\n\x1aSubmitBulkMessagesResponse\x12&\n\x08messages\x18\x01 \x03(\x0b\x32\x14.BulkMessageResponse\"\xa0\x04\n\x11StreamSyncRequest\x12#\n\x08get_info\x18\x01 \x01(\x0b\x32\x0f.HubInfoRequestH\x00\x12#\n\x11get_current_peers\x18\x02 \x01(\x0b\x32\x06.EmptyH\x00\x12\x1b\n\tstop_sync\x18\x03 \x01(\x0b\x32\x06.EmptyH\x00\x12(\n\nforce_sync\x18\x04 \x01(\x0b\x32\x12.SyncStatusRequestH\x00\x12-\n\x0fget_sync_status\x18\x05 \x01(\x0b\x32\x12.SyncStatusRequestH\x00\x12\x35\n\x1aget_all_sync_ids_by_prefix\x18\x06 \x01(\x0b\x32\x0f.TrieNodePrefixH\x00\x12\x30\n\x1cget_all_messages_by_sync_ids\x18\x07 \x01(\x0b\x32\x08.SyncIdsH\x00\x12\x36\n\x1bget_sync_metadata_by_prefix\x18\x08 \x01(\x0b\x32\x0f.TrieNodePrefixH\x00\x12\x36\n\x1bget_sync_snapshot_by_prefix\x18\t \x01(\x0b\x32\x0f.TrieNodePrefixH\x00\x12\x33\n\x13get_on_chain_events\x18\n \x01(\x0b\x32\x14.OnChainEventRequestH\x00\x12\x32\n\x1bget_on_chain_signers_by_fid\x18\x0b \x01(\x0b\x32\x0b.FidRequestH\x00\x42\t\n\x07request\"@\n\x0bStreamError\x12\x0f\n\x07\x65rrCode\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0f\n\x07request\x18\x03 \x01(\t\"\x80\x05\n\x12StreamSyncResponse\x12$\n\x08get_info\x18\x01 \x01(\x0b\x32\x10.HubInfoResponseH\x00\x12\x31\n\x11get_current_peers\x18\x02 \x01(\x0b\x32\x14.ContactInfoResponseH\x00\x12(\n\tstop_sync\x18\x03 \x01(\x0b\x32\x13.SyncStatusResponseH\x00\x12)\n\nforce_sync\x18\x04 \x01(\x0b\x32\x13.SyncStatusResponseH\x00\x12.\n\x0fget_sync_status\x18\x05 \x01(\x0b\x32\x13.SyncStatusResponseH\x00\x12.\n\x1aget_all_sync_ids_by_prefix\x18\x06 \x01(\x0b\x32\x08.SyncIdsH\x00\x12\x39\n\x1cget_all_messages_by_sync_ids\x18\x07 \x01(\x0b\x32\x11.MessagesResponseH\x00\x12@\n\x1bget_sync_metadata_by_prefix\x18\x08 \x01(\x0b\x32\x19.TrieNodeMetadataResponseH\x00\x12@\n\x1bget_sync_snapshot_by_prefix\x18\t \x01(\x0b\x32\x19.TrieNodeSnapshotResponseH\x00\x12\x34\n\x13get_on_chain_events\x18\n \x01(\x0b\x32\x15.OnChainEventResponseH\x00\x12<\n\x1bget_on_chain_signers_by_fid\x18\x0b \x01(\x0b\x32\x15.OnChainEventResponseH\x00\x12\x1d\n\x05\x65rror\x18\x0c \x01(\x0b\x32\x0c.StreamErrorH\x00\x42\n\n\x08response\"\xd7\x02\n\x12StreamFetchRequest\x12\x17\n\x0fidempotency_key\x18\x01 \x01(\t\x12\x34\n\x14\x63\x61st_messages_by_fid\x18\x02 \x01(\x0b\x32\x14.FidTimestampRequestH\x00\x12\x38\n\x18reaction_messages_by_fid\x18\x03 \x01(\x0b\x32\x14.FidTimestampRequestH\x00\x12<\n\x1cverification_messages_by_fid\x18\x04 \x01(\x0b\x32\x14.FidTimestampRequestH\x00\x12\x39\n\x19user_data_messages_by_fid\x18\x05 \x01(\x0b\x32\x14.FidTimestampRequestH\x00\x12\x34\n\x14link_messages_by_fid\x18\x06 \x01(\x0b\x32\x14.FidTimestampRequestH\x00\x42\t\n\x07request\"\x80\x01\n\x13StreamFetchResponse\x12\x17\n\x0fidempotency_key\x18\x01 \x01(\t\x12%\n\x08messages\x18\x02 \x01(\x0b\x32\x11.MessagesResponseH\x00\x12\x1d\n\x05\x65rror\x18\x03 \x01(\x0b\x32\x0c.StreamErrorH\x00\x42\n\n\x08response*\xbe\x01\n\tStoreType\x12\x13\n\x0fSTORE_TYPE_NONE\x10\x00\x12\x14\n\x10STORE_TYPE_CASTS\x10\x01\x12\x14\n\x10STORE_TYPE_LINKS\x10\x02\x12\x18\n\x14STORE_TYPE_REACTIONS\x10\x03\x12\x18\n\x14STORE_TYPE_USER_DATA\x10\x04\x12\x1c\n\x18STORE_TYPE_VERIFICATIONS\x10\x05\x12\x1e\n\x1aSTORE_TYPE_USERNAME_PROOFS\x10\x06*;\n\x0fStorageUnitType\x12\x14\n\x10UNIT_TYPE_LEGACY\x10\x00\x12\x12\n\x0eUNIT_TYPE_2024\x10\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'request_response_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STORETYPE']._serialized_start=6460
  _globals['_STORETYPE']._serialized_end=6650
  _globals['_STORAGEUNITTYPE']._serialized_start=6652
  _globals['_STORAGEUNITTYPE']._serialized_end=6711
  _globals['_EMPTY']._serialized_start=115
  _globals['_EMPTY']._serialized_end=122
  _globals['_SUBSCRIBEREQUEST']._serialized_start=125
  _globals['_SUBSCRIBEREQUEST']._serialized_end=299
  _globals['_EVENTREQUEST']._serialized_start=301
  _globals['_EVENTREQUEST']._serialized_end=327
  _globals['_HUBINFOREQUEST']._serialized_start=329
  _globals['_HUBINFOREQUEST']._serialized_end=363
  _globals['_HUBINFORESPONSE']._serialized_start=366
  _globals['_HUBINFORESPONSE']._serialized_end=527
  _globals['_DBSTATS']._serialized_start=529
  _globals['_DBSTATS']._serialized_end=631
  _globals['_SYNCSTATUSREQUEST']._serialized_start=633
  _globals['_SYNCSTATUSREQUEST']._serialized_end=684
  _globals['_SYNCSTATUSRESPONSE']._serialized_start=686
  _globals['_SYNCSTATUSRESPONSE']._serialized_end=784
  _globals['_SYNCSTATUS']._serialized_start=787
  _globals['_SYNCSTATUS']._serialized_end=987
  _globals['_TRIENODEMETADATARESPONSE']._serialized_start=989
  _globals['_TRIENODEMETADATARESPONSE']._serialized_end=1112
  _globals['_TRIENODESNAPSHOTRESPONSE']._serialized_start=1114
  _globals['_TRIENODESNAPSHOTRESPONSE']._serialized_end=1222
  _globals['_TRIENODEPREFIX']._serialized_start=1224
  _globals['_TRIENODEPREFIX']._serialized_end=1256
  _globals['_SYNCIDS']._serialized_start=1258
  _globals['_SYNCIDS']._serialized_end=1285
  _globals['_FIDREQUEST']._serialized_start=1288
  _globals['_FIDREQUEST']._serialized_end=1425
  _globals['_FIDTIMESTAMPREQUEST']._serialized_start=1428
  _globals['_FIDTIMESTAMPREQUEST']._serialized_end=1672
  _globals['_FIDSREQUEST']._serialized_start=1674
  _globals['_FIDSREQUEST']._serialized_end=1799
  _globals['_FIDSRESPONSE']._serialized_start=1801
  _globals['_FIDSRESPONSE']._serialized_end=1879
  _globals['_MESSAGESRESPONSE']._serialized_start=1881
  _globals['_MESSAGESRESPONSE']._serialized_end=1977
  _globals['_CASTSBYPARENTREQUEST']._serialized_start=1980
  _globals['_CASTSBYPARENTREQUEST']._serialized_end=2181
  _globals['_REACTIONREQUEST']._serialized_start=2184
  _globals['_REACTIONREQUEST']._serialized_end=2319
  _globals['_REACTIONSBYFIDREQUEST']._serialized_start=2322
  _globals['_REACTIONSBYFIDREQUEST']._serialized_end=2531
  _globals['_REACTIONSBYTARGETREQUEST']._serialized_start=2534
  _globals['_REACTIONSBYTARGETREQUEST']._serialized_end=2800
  _globals['_USERDATAREQUEST']._serialized_start=2802
  _globals['_USERDATAREQUEST']._serialized_end=2871
  _globals['_NAMEREGISTRYEVENTREQUEST']._serialized_start=2873
  _globals['_NAMEREGISTRYEVENTREQUEST']._serialized_end=2913
  _globals['_RENTREGISTRYEVENTSREQUEST']._serialized_start=2915
  _globals['_RENTREGISTRYEVENTSREQUEST']._serialized_end=2955
  _globals['_ONCHAINEVENTREQUEST']._serialized_start=2958
  _globals['_ONCHAINEVENTREQUEST']._serialized_end=3143
  _globals['_ONCHAINEVENTRESPONSE']._serialized_start=3145
  _globals['_ONCHAINEVENTRESPONSE']._serialized_end=3248
  _globals['_STORAGELIMITSRESPONSE']._serialized_start=3250
  _globals['_STORAGELIMITSRESPONSE']._serialized_end=3362
  _globals['_STORAGEUNITDETAILS']._serialized_start=3364
  _globals['_STORAGEUNITDETAILS']._serialized_end=3440
  _globals['_STORAGELIMIT']._serialized_start=3443
  _globals['_STORAGELIMIT']._serialized_end=3581
  _globals['_USERNAMEPROOFREQUEST']._serialized_start=3583
  _globals['_USERNAMEPROOFREQUEST']._serialized_end=3619
  _globals['_USERNAMEPROOFSRESPONSE']._serialized_start=3621
  _globals['_USERNAMEPROOFSRESPONSE']._serialized_end=3677
  _globals['_VERIFICATIONREQUEST']._serialized_start=3679
  _globals['_VERIFICATIONREQUEST']._serialized_end=3730
  _globals['_SIGNERREQUEST']._serialized_start=3732
  _globals['_SIGNERREQUEST']._serialized_end=3776
  _globals['_LINKREQUEST']._serialized_start=3778
  _globals['_LINKREQUEST']._serialized_end=3855
  _globals['_LINKSBYFIDREQUEST']._serialized_start=3858
  _globals['_LINKSBYFIDREQUEST']._serialized_end=4040
  _globals['_LINKSBYTARGETREQUEST']._serialized_start=4043
  _globals['_LINKSBYTARGETREQUEST']._serialized_end=4247
  _globals['_IDREGISTRYEVENTBYADDRESSREQUEST']._serialized_start=4249
  _globals['_IDREGISTRYEVENTBYADDRESSREQUEST']._serialized_end=4299
  _globals['_CONTACTINFORESPONSE']._serialized_start=4301
  _globals['_CONTACTINFORESPONSE']._serialized_end=4365
  _globals['_VALIDATIONRESPONSE']._serialized_start=4367
  _globals['_VALIDATIONRESPONSE']._serialized_end=4429
  _globals['_SUBMITBULKMESSAGESREQUEST']._serialized_start=4431
  _globals['_SUBMITBULKMESSAGESREQUEST']._serialized_end=4486
  _globals['_MESSAGEERROR']._serialized_start=4488
  _globals['_MESSAGEERROR']._serialized_end=4550
  _globals['_BULKMESSAGERESPONSE']._serialized_start=4552
  _globals['_BULKMESSAGERESPONSE']._serialized_end=4654
  _globals['_SUBMITBULKMESSAGESRESPONSE']._serialized_start=4656
  _globals['_SUBMITBULKMESSAGESRESPONSE']._serialized_end=4724
  _globals['_STREAMSYNCREQUEST']._serialized_start=4727
  _globals['_STREAMSYNCREQUEST']._serialized_end=5271
  _globals['_STREAMERROR']._serialized_start=5273
  _globals['_STREAMERROR']._serialized_end=5337
  _globals['_STREAMSYNCRESPONSE']._serialized_start=5340
  _globals['_STREAMSYNCRESPONSE']._serialized_end=5980
  _globals['_STREAMFETCHREQUEST']._serialized_start=5983
  _globals['_STREAMFETCHREQUEST']._serialized_end=6326
  _globals['_STREAMFETCHRESPONSE']._serialized_start=6329
  _globals['_STREAMFETCHRESPONSE']._serialized_end=6457
# @@protoc_insertion_point(module_scope)
