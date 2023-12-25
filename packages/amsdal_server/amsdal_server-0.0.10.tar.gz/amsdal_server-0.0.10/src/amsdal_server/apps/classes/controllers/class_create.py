from fastapi import Request

from amsdal_server.apps.classes.router import router
from amsdal_server.apps.classes.serializers.class_info import ClassInfo
from amsdal_server.apps.classes.serializers.register_class import RegisterClassData
from amsdal_server.apps.classes.services.classes_api import ClassesApi


@router.post('/api/classes/', description='Register a class.')
async def class_create(
    request: Request,
    data: RegisterClassData,
) -> ClassInfo:
    return ClassesApi.register_class(request.user, data)
