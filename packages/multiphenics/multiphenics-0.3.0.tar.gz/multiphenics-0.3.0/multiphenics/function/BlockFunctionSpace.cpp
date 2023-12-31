// Copyright (C) 2016-2022 by the multiphenics authors
//
// This file is part of multiphenics.
//
// multiphenics is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// multiphenics is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with multiphenics. If not, see <http://www.gnu.org/licenses/>.
//

#include <multiphenics/function/BlockFunctionSpace.h>

using namespace dolfin;
using namespace multiphenics;

//-----------------------------------------------------------------------------
BlockFunctionSpace::BlockFunctionSpace(std::vector<std::shared_ptr<const FunctionSpace>> function_spaces)
  : Hierarchical<BlockFunctionSpace>(*this),
    _restrictions(function_spaces.size()), _function_spaces(function_spaces), _root_space_id(id())
{
  _init_mesh_and_elements_and_dofmaps_from_function_spaces();
  _init_block_dofmap_from_dofmaps_and_restrictions();
}
//-----------------------------------------------------------------------------
BlockFunctionSpace::BlockFunctionSpace(std::vector<std::shared_ptr<const FunctionSpace>> function_spaces,
                                       std::vector<std::vector<std::shared_ptr<const MeshFunction<bool>>>> restrictions)
  : Hierarchical<BlockFunctionSpace>(*this),
    _restrictions(restrictions), _function_spaces(function_spaces), _root_space_id(id())
{
  _init_mesh_and_elements_and_dofmaps_from_function_spaces();
  _init_block_dofmap_from_dofmaps_and_restrictions();
}
//-----------------------------------------------------------------------------
BlockFunctionSpace::BlockFunctionSpace(std::shared_ptr<const Mesh> mesh,
                                       std::vector<std::shared_ptr<const FiniteElement>> elements,
                                       std::vector<std::shared_ptr<const GenericDofMap>> dofmaps)
  : Hierarchical<BlockFunctionSpace>(*this),
    _mesh(mesh), _elements(elements), _dofmaps(dofmaps), _restrictions(dofmaps.size()), _root_space_id(id())
{
  _init_function_spaces_from_elements_and_dofmaps();
  _init_block_dofmap_from_dofmaps_and_restrictions();
}
//-----------------------------------------------------------------------------
BlockFunctionSpace::BlockFunctionSpace(std::shared_ptr<const Mesh> mesh,
                                       std::vector<std::shared_ptr<const FiniteElement>> elements,
                                       std::vector<std::shared_ptr<const GenericDofMap>> dofmaps,
                                       std::vector<std::vector<std::shared_ptr<const MeshFunction<bool>>>> restrictions)
  : Hierarchical<BlockFunctionSpace>(*this),
    _mesh(mesh), _elements(elements), _dofmaps(dofmaps), _restrictions(restrictions), _root_space_id(id())
{
  _init_function_spaces_from_elements_and_dofmaps();
  _init_block_dofmap_from_dofmaps_and_restrictions();
}
//-----------------------------------------------------------------------------
BlockFunctionSpace::BlockFunctionSpace(const BlockFunctionSpace& V)
  : Hierarchical<BlockFunctionSpace>(*this)
{
  // Assign data (will be shared)
  *this = V;
}
//-----------------------------------------------------------------------------
BlockFunctionSpace::~BlockFunctionSpace()
{
  // Do nothing
}
//-----------------------------------------------------------------------------
void BlockFunctionSpace::_init_mesh_and_elements_and_dofmaps_from_function_spaces() {
  _mesh = _function_spaces[0]->mesh();
  for (auto& function_space : _function_spaces) 
  {
    dolfin_assert(_mesh == function_space->mesh());
    _elements.push_back(function_space->element());
    _dofmaps.push_back(function_space->dofmap());
  }
}
//-----------------------------------------------------------------------------
void BlockFunctionSpace::_init_function_spaces_from_elements_and_dofmaps() {
  dolfin_assert(_elements.size() == _dofmaps.size());
  for (unsigned int i(0); i < _elements.size(); ++i) 
  {
    std::shared_ptr<const FunctionSpace> function_space_i(new FunctionSpace(_mesh, _elements[i], _dofmaps[i]));
    _function_spaces.push_back(function_space_i);
  }
}
//-----------------------------------------------------------------------------
void BlockFunctionSpace::_init_block_dofmap_from_dofmaps_and_restrictions() {
  _block_dofmap = std::make_shared<BlockDofMap>(_dofmaps, _restrictions, *_mesh);
}
//-----------------------------------------------------------------------------
const BlockFunctionSpace& BlockFunctionSpace::operator=(const BlockFunctionSpace& V)
{
  // Assign data (will be shared)
  _mesh            = V._mesh;
  _elements        = V._elements;
  _dofmaps         = V._dofmaps;
  _restrictions    = V._restrictions;
  _function_spaces = V._function_spaces;
  _block_dofmap    = V._block_dofmap;
  _component       = V._component;

  // Call assignment operator for base class
  Variable::operator=(V);
  Hierarchical<BlockFunctionSpace>::operator=(V);

  return *this;
}
//-----------------------------------------------------------------------------
bool BlockFunctionSpace::operator==(const BlockFunctionSpace& V) const
{
  // Compare pointers to shared objects
  
  // -> elements
  if (_elements.size() != V._elements.size())
    return false;
  for (unsigned int i(0); i < _elements.size(); ++i)
    if (_elements[i].get() != V._elements[i].get())
      return false;
      
  // -> dofmaps
  if (_dofmaps.size() != V._dofmaps.size())
    return false;
  for (unsigned int i(0); i < _dofmaps.size(); ++i)
    if (_dofmaps[i].get() != V._dofmaps[i].get())
      return false;
      
  // -> restrictions
  if (_restrictions.size() != V._restrictions.size())
    return false;
  for (unsigned int i(0); i < _restrictions.size(); ++i)
    for (unsigned int d(0); d < _restrictions[i].size(); ++d)
      if (_restrictions[i][d].get() != V._restrictions[i][d].get())
        return false;
      
  // -> function_spaces
  if (_function_spaces.size() != V._function_spaces.size())
    return false;
  for (unsigned int i(0); i < _function_spaces.size(); ++i)
    if (_function_spaces[i].get() != V._function_spaces[i].get())
      return false;
      
  // -> mesh and block_dofmap
  return 
    _mesh.get() == V._mesh.get() &&
    _block_dofmap.get() == V._block_dofmap.get();
}
//-----------------------------------------------------------------------------
bool BlockFunctionSpace::operator!=(const BlockFunctionSpace& V) const
{
  // Compare pointers to shared objects
  return !(*this == V);
}
//-----------------------------------------------------------------------------
std::shared_ptr<const Mesh> BlockFunctionSpace::mesh() const
{
  return _mesh;
}
//-----------------------------------------------------------------------------
std::vector<std::shared_ptr<const FiniteElement>> BlockFunctionSpace::elements() const
{
  return _elements;
}
//-----------------------------------------------------------------------------
std::vector<std::shared_ptr<const GenericDofMap>> BlockFunctionSpace::dofmaps() const
{
  return _dofmaps;
}
//-----------------------------------------------------------------------------
std::shared_ptr<const BlockDofMap> BlockFunctionSpace::block_dofmap() const
{
  return _block_dofmap;
}
//-----------------------------------------------------------------------------
std::vector<std::shared_ptr<const FunctionSpace>> BlockFunctionSpace::function_spaces() const
{
  return _function_spaces;
}
//-----------------------------------------------------------------------------
std::size_t BlockFunctionSpace::dim() const
{
  dolfin_assert(_block_dofmap);
  return _block_dofmap->global_dimension();
}
//-----------------------------------------------------------------------------
std::shared_ptr<const FunctionSpace> BlockFunctionSpace::operator[] (std::size_t i) const
{
  return _function_spaces[i];
}
//-----------------------------------------------------------------------------
std::shared_ptr<const FunctionSpace> BlockFunctionSpace::sub(std::size_t i) const
{
  return _function_spaces[i];
}
//-----------------------------------------------------------------------------
std::shared_ptr<BlockFunctionSpace>
BlockFunctionSpace::extract_block_sub_space(const std::vector<std::size_t>& component, bool with_restrictions) const
{
  dolfin_assert(_mesh);

  // Check if sub space is already in the cache
  BlockSubpsacesType* block_subspaces;
  if (with_restrictions)
    block_subspaces = &_block_subspaces__with_restrictions;
  else
    block_subspaces = &_block_subspaces__without_restrictions;
  BlockSubpsacesType::const_iterator subspace = block_subspaces->find(component);
  if (subspace != block_subspaces->end())
    return subspace->second;
  else
  {
    // Extract sub elements
    std::vector<std::shared_ptr<const FiniteElement>> sub_elements;
    for (auto c: component)
      sub_elements.push_back(_elements[c]);

    // Extract sub dofmaps
    std::vector<std::shared_ptr<const GenericDofMap>> sub_dofmaps;
    for (auto c: component)
      sub_dofmaps.push_back(_dofmaps[c]);

    // Extract restrictions, if required
    std::vector<std::vector<std::shared_ptr<const MeshFunction<bool>>>> sub_restrictions;
    if (with_restrictions)
      for (auto c: component)
        sub_restrictions.push_back(_restrictions[c]);
    
    // Create new block sub space
    std::shared_ptr<BlockFunctionSpace>
      new_block_sub_space(new BlockFunctionSpace(_mesh, sub_elements, sub_dofmaps, sub_restrictions));

    // Set root space id and component w.r.t. root
    new_block_sub_space->_root_space_id = _root_space_id;
    auto& new_component = new_block_sub_space->_component;
    new_component.clear();
    new_component.insert(new_component.end(), _component.begin(), _component.end());
    new_component.insert(new_component.end(), component.begin(), component.end());

    // Insert new sub space into cache
    block_subspaces->insert(std::pair<std::vector<std::size_t>, std::shared_ptr<BlockFunctionSpace>>(
                              component, new_block_sub_space
                            ));

    return new_block_sub_space;
  }
}
//-----------------------------------------------------------------------------
std::vector<std::size_t> BlockFunctionSpace::component() const
{
  return _component;
}
//-----------------------------------------------------------------------------
std::string BlockFunctionSpace::str(bool verbose) const
{
  std::stringstream s;

  if (verbose)
  {
    s << str(false) << std::endl << std::endl;

    // No verbose output implemented
  }
  else
    s << "<BlockFunctionSpace of dimension " << dim() << ">";

  return s.str();
}
//-----------------------------------------------------------------------------
bool BlockFunctionSpace::contains(const BlockFunctionSpace& V) const
{
  // Is the root space same?
  if (_root_space_id != V._root_space_id)
    return false;

  // Is V possibly our superspace?
  if (_component.size() > V._component.size())
    return false;

  // Are our components same as leading components of V?
  for (std::size_t i = 0; i < _component.size(); ++i)
  {
    if (_component[i] != V._component[i])
      return false;
  }

  // Ok, V is really our subspace
  return true;
}
//-----------------------------------------------------------------------------
std::vector<double> BlockFunctionSpace::tabulate_dof_coordinates() const
{
  // Geometric dimension
  dolfin_assert(_mesh);
  const std::size_t gdim = _mesh->geometry().dim();
  
  // Get local size
  dolfin_assert(_block_dofmap);
  std::size_t local_size = _block_dofmap->index_map()->size(IndexMap::MapSize::OWNED);
  
  // Vector to hold coordinates and return
  std::vector<double> dof_coordinates(gdim*local_size);
  
  // Loop over subspaces
  for (unsigned int i(0); i < _function_spaces.size(); ++i)
  {
    auto function_space = _function_spaces[i];
    
    // Get dof coordinates of function space
    auto sub_dof_coordinates = function_space->tabulate_dof_coordinates();
    
    // Get original to block numbering
    auto original_to_block = _block_dofmap->original_to_block(i);
    
    // Loop over all original dofs
    for (unsigned int d(0); d < sub_dof_coordinates.size()/gdim; ++d)
    {
      if (original_to_block.count(d) > 0) // skip all dofs which have been removed by restriction
      {
        for (std::size_t c(0); c < gdim; ++c)
        {
          dof_coordinates[gdim*original_to_block.at(d) + c] = sub_dof_coordinates[gdim*d + c];
        }
      }
    }
  }
  
  return dof_coordinates;
}
//-----------------------------------------------------------------------------
