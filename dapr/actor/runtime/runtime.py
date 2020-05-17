# -*- coding: utf-8 -*-

"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT License.
"""

import asyncio

from typing import List

from dapr.actor.id import ActorId
from dapr.actor.runtime.actor import Actor
from dapr.actor.runtime.config import ActorRuntimeConfig
from dapr.actor.runtime.context import ActorRuntimeContext
from dapr.actor.runtime.type_information import ActorTypeInformation
from dapr.actor.runtime.manager import ActorManager
from dapr.clients import DaprActorHttpClient
from dapr.serializers import Serializer, DefaultJSONSerializer


class ActorRuntime:
    """The class that creates instances of :class:`Actor` and
    activates and deactivates :class:`Actor`.
    """

    _actor_config = ActorRuntimeConfig()

    _actor_managers = {}
    _actor_managers_lock = asyncio.Lock()

    @classmethod
    async def register_actor(
            cls, actor: Actor,
            message_serializer: Serializer = DefaultJSONSerializer(),
            state_serializer: Serializer = DefaultJSONSerializer()) -> None:
        """Registers an :class:`Actor` with the runtime.

        Args:
            actor (:class:`Actor`): Actor implementation.
            message_serializer (:class:`Serializer`): A serializer that serializes message
                between actors.
            state_serializer (:class:`Serializer`): Serializer that serializes state values.
        """
        type_info = ActorTypeInformation.create(actor)
        # TODO: We will allow to use gRPC client later.
        actor_client = DaprActorHttpClient()
        ctx = ActorRuntimeContext(type_info, message_serializer, state_serializer, actor_client)

        # Create an ActorManager, override existing entry if registered again.
        async with cls._actor_managers_lock:
            cls._actor_managers[type_info.type_name] = ActorManager(ctx)
            cls._actor_config.update_entities(ActorRuntime.get_registered_actor_types())

    @classmethod
    def get_registered_actor_types(cls) -> List[str]:
        """Gets registered actor types."""
        return [actor_type for actor_type in cls._actor_managers.keys()]

    @classmethod
    async def activate(cls, actor_type_name: str, actor_id: str) -> None:
        """Activates an actor for an actor type with given actor id.

        Args:
            actor_type_name (str): the name of actor type.
            actor_id (str): the actor id.
        """
        manager = await cls._get_actor_manager(actor_type_name)
        await manager.activate_actor(ActorId(actor_id))

    @classmethod
    async def deactivate(cls, actor_type_name: str, actor_id: str) -> None:
        """Deactivates an actor for an actor type with given actor id.

        Args:
            actor_type_name (str): the name of actor type.
            actor_id (str): the actor id.
        """
        manager = await cls._get_actor_manager(actor_type_name)
        await manager.deactivate_actor(ActorId(actor_id))

    @classmethod
    async def dispatch(
            cls, actor_type_name: str, actor_id: str,
            actor_method_name: str, request_body: bytes) -> bytes:
        """Dispatches actor method defined in actor_type.

        Args:
            actor_type_name (str): the name of actor type.
            actor_id (str): Actor ID.
            actor_method_name (str): the method name that is dispatched.
            request_body (bytes): the body of request that is passed to actor method arguments.

        Returns:
            bytes: serialized response data.
        """
        manager = await cls._get_actor_manager(actor_type_name)
        return await manager.dispatch(ActorId(actor_id), actor_method_name, request_body)

    @classmethod
    async def fire_reminder(
            cls, actor_type_name: str, actor_id: str,
            name: str, request_body: bytes) -> None:
        """Fires a reminder for the Actor.

        Args:
            actor_type_name (str): the name of actor type.
            actor_id (str): Actor ID.
            name (str): the name of reminder.
            request_body (bytes): the body of request that is passed to reminder callback.
        """

        manager = await cls._get_actor_manager(actor_type_name)
        await manager.fire_reminder(ActorId(actor_id), name, request_body)

    @classmethod
    async def fire_timer(cls, actor_type_name: str, actor_id: str, name: str) -> None:
        """Fires a timer for the Actor.

        Args:
            actor_type_name (str): the name of actor type.
            actor_id (str): Actor ID.
            name (str): the timer name.
        """
        manager = await cls._get_actor_manager(actor_type_name)
        await manager.fire_timer(ActorId(actor_id), name)

    @classmethod
    def set_actor_config(cls, config: ActorRuntimeConfig) -> None:
        """Sets actor runtime config

        :param ActorRuntimeConfig config: The config to set up actor runtime
        """
        cls._actor_config = config
        cls._actor_config.update_entities(ActorRuntime.get_registered_actor_types())

    @classmethod
    def get_actor_config(cls) -> ActorRuntimeConfig:
        """Gets :class:`ActorRuntimeConfig`."""
        return cls._actor_config

    @classmethod
    async def _get_actor_manager(cls, actor_type_name: str) -> ActorManager:
        """Gets :class:`ActorManager` for actor_type_name.

        Args:
            actor_type_name (str): the type name of actor.

        Returns:
            :class:`ActorManager`: an actor manager object for actor_type_name actor.
        """
        async with cls._actor_managers_lock:
            return cls._actor_managers.get(actor_type_name)
