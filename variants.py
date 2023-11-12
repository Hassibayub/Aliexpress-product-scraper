def get(skuModule):
    
    skuModule = skuModule[0]
    
    priceLists = skuModule.get('skuPriceList', [])
    optionsLists = skuModule.get('productSKUPropertyList', [])

    options = [
        {
            'id': lst['skuPropertyId'],
            'name': lst['skuPropertyName'],
            'values': [
                {
                    'id': val['propertyValueId'],
                    'name': val['propertyValueName'],
                    'displayName': val['propertyValueDisplayName'],
                    'image': val.get('skuPropertyImagePath', None)
                }
                for val in lst['skuPropertyValues']
            ]
        }
        for lst in optionsLists
    ]

    lists = [
        {
            'skuId': lst['skuId'],
            'optionValueIds': lst['skuPropIds'],
            'availableQuantity': lst['skuVal'].get('availQuantity', None),
            'originalPrice': lst['skuVal']['skuAmount']['value'],
            'salePrice': lst['skuVal']['skuActivityAmount']['value']
        }
        for lst in priceLists
    ]

    return {
        'options': options,
        'prices': lists
    }
