# pylint: disable
# flake8: noqa
from __future__ import annotations
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from llamazure.azrest.models import AzList, ReadOnly, Req
class ValidationResponseErrorInfo(BaseModel):
	"""Failed validation result details"""

	code: ReadOnly[str] = None
	message: ReadOnly[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
		)



class ValidationResponse(BaseModel):
	"""Validation response"""

	isValid: ReadOnly[bool] = None
	errorInfo: ValidationResponseErrorInfo

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.errorInfo == o.errorInfo
		)



class RoleAssignmentFilter(BaseModel):
	"""Role Assignments filter"""

	principalId: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.principalId == o.principalId
		)



class RoleAssignment(BaseModel):
	"""Role Assignments"""
	class Properties(BaseModel):
		"""Role assignment properties."""

		scope: ReadOnly[str] = None
		roleDefinitionId: Optional[str] = None
		principalId: Optional[str] = None
		principalType: Optional[str] = None
		description: Optional[str] = None
		condition: Optional[str] = None
		conditionVersion: Optional[str] = None
		createdOn: ReadOnly[str] = None
		updatedOn: ReadOnly[str] = None
		createdBy: ReadOnly[str] = None
		updatedBy: ReadOnly[str] = None
		delegatedManagedIdentityResourceId: Optional[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.roleDefinitionId == o.roleDefinitionId
				and self.principalId == o.principalId
				and self.principalType == o.principalType
				and self.description == o.description
				and self.condition == o.condition
				and self.conditionVersion == o.conditionVersion
				and self.delegatedManagedIdentityResourceId == o.delegatedManagedIdentityResourceId
			)


	rid: ReadOnly[str] = Field(alias="id", default=None)
	name: ReadOnly[str] = None
	type: ReadOnly[str] = None
	properties: Properties

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.properties == o.properties
		)



class RoleAssignmentCreateParameters(BaseModel):
	"""Role assignment create parameters."""
	class Properties(BaseModel):
		"""Role assignment properties."""

		scope: ReadOnly[str] = None
		roleDefinitionId: Optional[str] = None
		principalId: Optional[str] = None
		principalType: Optional[str] = None
		description: Optional[str] = None
		condition: Optional[str] = None
		conditionVersion: Optional[str] = None
		createdOn: ReadOnly[str] = None
		updatedOn: ReadOnly[str] = None
		createdBy: ReadOnly[str] = None
		updatedBy: ReadOnly[str] = None
		delegatedManagedIdentityResourceId: Optional[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.roleDefinitionId == o.roleDefinitionId
				and self.principalId == o.principalId
				and self.principalType == o.principalType
				and self.description == o.description
				and self.condition == o.condition
				and self.conditionVersion == o.conditionVersion
				and self.delegatedManagedIdentityResourceId == o.delegatedManagedIdentityResourceId
			)


	properties: Properties

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.properties == o.properties
		)



RoleAssignmentListResult = AzList[RoleAssignment]

ValidationResponseErrorInfo.model_rebuild()

ValidationResponse.model_rebuild()

RoleAssignmentFilter.model_rebuild()

RoleAssignment.model_rebuild()

RoleAssignmentCreateParameters.model_rebuild()

RoleAssignmentListResult.model_rebuild()

class AzRoleAssignments:
	apiv = "2022-04-01"
	@staticmethod
	def ListForSubscription(subscriptionId: str) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a subscription."""
		return Req.get(
			name="RoleAssignments.ListForSubscription",
			path=f"/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)

	@staticmethod
	def ListForResourceGroup(subscriptionId: str, resourceGroupName: str) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a resource group."""
		return Req.get(
			name="RoleAssignments.ListForResourceGroup",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)

	@staticmethod
	def ListForResource(subscriptionId: str, resourceGroupName: str, resourceProviderNamespace: str, resourceType: str, resourceName: str) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a resource."""
		return Req.get(
			name="RoleAssignments.ListForResource",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)

	@staticmethod
	def Get(scope: str, roleAssignmentName: str) -> Req[RoleAssignment]:
		"""Get a role assignment by scope and name."""
		return Req.get(
			name="RoleAssignments.Get",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments/{roleAssignmentName}",
			apiv="2022-04-01",
			ret_t=RoleAssignment
		)

	@staticmethod
	def Create(scope: str, roleAssignmentName: str, parameters: RoleAssignmentCreateParameters) -> Req[RoleAssignment]:
		"""Create or update a role assignment by scope and name."""
		return Req.put(
			name="RoleAssignments.Create",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments/{roleAssignmentName}",
			apiv="2022-04-01",
			body=parameters,
			ret_t=RoleAssignment
		)

	@staticmethod
	def Delete(scope: str, roleAssignmentName: str) -> Req[Optional[RoleAssignment]]:
		"""Delete a role assignment by scope and name."""
		return Req.delete(
			name="RoleAssignments.Delete",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments/{roleAssignmentName}",
			apiv="2022-04-01",
			ret_t=Optional[RoleAssignment]
		)

	@staticmethod
	def ListForScope(scope: str) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a scope."""
		return Req.get(
			name="RoleAssignments.ListForScope",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)

	@staticmethod
	def GetById(roleAssignmentId: str) -> Req[RoleAssignment]:
		"""Get a role assignment by ID."""
		return Req.get(
			name="RoleAssignments.GetById",
			path=f"/{roleAssignmentId}",
			apiv="2022-04-01",
			ret_t=RoleAssignment
		)

	@staticmethod
	def CreateById(roleAssignmentId: str, parameters: RoleAssignmentCreateParameters) -> Req[RoleAssignment]:
		"""Create or update a role assignment by ID."""
		return Req.put(
			name="RoleAssignments.CreateById",
			path=f"/{roleAssignmentId}",
			apiv="2022-04-01",
			body=parameters,
			ret_t=RoleAssignment
		)

	@staticmethod
	def DeleteById(roleAssignmentId: str) -> Req[Optional[RoleAssignment]]:
		"""Delete a role assignment by ID."""
		return Req.delete(
			name="RoleAssignments.DeleteById",
			path=f"/{roleAssignmentId}",
			apiv="2022-04-01",
			ret_t=Optional[RoleAssignment]
		)

