import ndf_parse as ndf

ERA_DAMAGE_REDUCTION = 4.0


def create_era_resist_type(dmg_resist, armor_desc):
    resist_type_expr = "TResistanceTypeRTTI(Family=\"era\" Index={index})"

    resist_types = dmg_resist[0].value[0]
    dmg_types = dmg_resist[0].value[1]
    dmg_values = dmg_resist[0].value[2]

    first_armor_index = -1
    last_armor_index = -1

    # get first and last armor index
    for i, resist in enumerate(resist_types.value):
        family = resist.value[0].value.removeprefix("\"").removesuffix("\"")

        if family == "blindage":
            if first_armor_index < 1:
                first_armor_index = i
            last_armor_index = i

    # add ERA resistance types to list
    for i in range(last_armor_index - first_armor_index):
        resist_type_dict = ndf.expression(resist_type_expr.format(index=i + 1))
        resist_types.value.add(**resist_type_dict)

    # add ERA damage table entries
    for i, dmg_type in enumerate(dmg_types.value):
        family = dmg_type.value[0].value.removeprefix("\"").removesuffix("\"")

        dmg_value = dmg_values.value[i].value
        armor_dmg_values = dmg_value[first_armor_index:last_armor_index + 1]

        for val in armor_dmg_values:
            dmg = float(val.value)
            # reduce damage against ERA by HEAT
            if family == "ap_missile":
                dmg = max(1.0, dmg - ERA_DAMAGE_REDUCTION)
            dmg_value.add(value=dmg)

    # add armor descriptors
    name_for_index = {}
    for armor in armor_desc:
        if armor.value.by_member("BaseBlindage").value.by_member("Family").value == '\"blindage\"':
            name = armor.value.by_member("Name").value
            index = int(armor.value.by_member("BaseBlindage").value.by_member("Index").value)
            name_for_index[index] = name

    armor_desc_expr = "export ArmorDescriptor_ERA_{index} is TArmorDescriptor\n(\n    Name         = {name}\n" \
                      "    BaseBlindage = TResistanceTypeRTTI(Family=\"era\" Index={index})\n)"

    for i in range(len(name_for_index)):
        ad_text = armor_desc_expr.format(index=i+1, name=name_for_index[i+1])
        ad_dict = ndf.expression(ad_text)
        armor_desc.add(**ad_dict)




