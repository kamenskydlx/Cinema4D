import c4d
from c4d import gui

"""
    made by Dmitry Kamensky
    https://t.me/kamensky

    Script will iterate through all materials in scene and check if there any Bitmap used.
    Works with [Diffuse, Roughness, Bump, Normal, Opacity] channels, finds Bitmaps connected directly to material inputs, 
    but also if [Multiply, Mix, ColorCorrection, Invert] node is used inbetween.
    
    Скрипт для исправления материалов, где вместо ImageTexutre использовался Bitmap
    Работает если:
    в каналы [Diffuse, Roughness, Bump, Normal, Opacity]
    подключена непосредственно Bitmap
    или Bitmap через [Multiply, Mix, ColorCorrection, Invert]
"""

ID_C4D_BITMAP = 5833

ID_OCT_MATERIAL = 1029501

ID_OCT_IMAGE_TEXTURE = 1029508
ID_OCT_COLORCORRECTION = 1029512
ID_OCT_INVERT_TEXTURE = 1029514
ID_OCT_MULTIPLY_TEXTURE = 1029516
ID_OCT_MIXTEXTURE = 1029505

def ReplaceBitmap(material, channel):
    node = material[channel]

    if node:
        node_type = node.GetType()

        if node_type == ID_C4D_BITMAP:
            texture_name = node[c4d.BITMAPSHADER_FILENAME]
            NewImgtex = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
            doc.InsertShader(NewImgtex)
            material[channel] = NewImgtex
            NewImgtex[c4d.IMAGETEXTURE_FILE] = texture_name
            node.Remove()


        if node_type == ID_OCT_MULTIPLY_TEXTURE:
            if node[c4d.MULTIPLY_TEXTURE1].GetType() == ID_C4D_BITMAP:
                bitmap1 = node[c4d.MULTIPLY_TEXTURE1]
                texture_name1 = bitmap1[c4d.BITMAPSHADER_FILENAME]
                NewImgtex1 = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
                doc.InsertShader(NewImgtex1)
                node[c4d.MULTIPLY_TEXTURE1] = NewImgtex1
                NewImgtex1[c4d.IMAGETEXTURE_FILE] = texture_name1
                bitmap1.Remove()
            if node[c4d.MULTIPLY_TEXTURE2].GetType() == ID_C4D_BITMAP:
                bitmap2 = node[c4d.MULTIPLY_TEXTURE2]
                texture_name2 = bitmap2[c4d.BITMAPSHADER_FILENAME]
                NewImgtex2 = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
                doc.InsertShader(NewImgtex2)
                node = NewImgtex2
                NewImgtex2[c4d.IMAGETEXTURE_FILE] = texture_name2
                bitmap2.Remove()

        if node_type == ID_OCT_MIXTEXTURE:
            if node[c4d.MIXTEX_AMOUNT_LNK]:
                if node[c4d.MIXTEX_AMOUNT_LNK].GetType() == ID_C4D_BITMAP:
                    bitmap0 = node[c4d.MIXTEX_AMOUNT_LNK]
                    texture_name0 = bitmap0[c4d.BITMAPSHADER_FILENAME]
                    NewImgtex0 = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
                    doc.InsertShader(NewImgtex0)
                    node[c4d.MIXTEX_AMOUNT_LNK] = NewImgtex0
                    NewImgtex0[c4d.IMAGETEXTURE_FILE] = texture_name0
                    bitma0p.Remove()
            if node[c4d.MIXTEX_TEXTURE1_LNK]:
                if node[c4d.MIXTEX_TEXTURE1_LNK].GetType() == ID_C4D_BITMAP:
                    bitmap1 = node[c4d.MIXTEX_TEXTURE1_LNK]
                    texture_name1 = bitmap1[c4d.BITMAPSHADER_FILENAME]
                    NewImgtex1 = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
                    doc.InsertShader(NewImgtex1)
                    node[c4d.MIXTEX_TEXTURE1_LNK] = NewImgtex1
                    NewImgtex1[c4d.IMAGETEXTURE_FILE] = texture_name1
                    bitmap1.Remove()
            if node[c4d.MIXTEX_TEXTURE2_LNK]:
                if node[c4d.MIXTEX_TEXTURE2_LNK].GetType() == ID_C4D_BITMAP:
                    bitmap2 = node[c4d.MIXTEX_TEXTURE2_LNK]
                    texture_name2 = bitmap2[c4d.BITMAPSHADER_FILENAME]
                    NewImgtex2 = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
                    doc.InsertShader(NewImgtex2)
                    node[c4d.MIXTEX_TEXTURE2_LNK] = NewImgtex2
                    NewImgtex2[c4d.IMAGETEXTURE_FILE] = texture_name2
                    bitmap2.Remove()



        if node_type == ID_OCT_COLORCORRECTION:
            if node[c4d.COLORCOR_TEXTURE_LNK].GetType() == ID_C4D_BITMAP:
                bitmap = node[c4d.COLORCOR_TEXTURE_LNK]
                texture_name = bitmap[c4d.BITMAPSHADER_FILENAME]
                NewImgtex = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
                doc.InsertShader(NewImgtex)
                node[c4d.COLORCOR_TEXTURE_LNK] = NewImgtex
                NewImgtex[c4d.IMAGETEXTURE_FILE] = texture_name
                bitmap.Remove()

        if node_type == ID_OCT_INVERT_TEXTURE:
            if node[c4d.INVERT_TEXTURE].GetType() == ID_C4D_BITMAP:
                bitmap = node[c4d.INVERT_TEXTURE]
                texture_name = bitmap[c4d.BITMAPSHADER_FILENAME]
                NewImgtex = c4d.BaseShader(ID_OCT_IMAGE_TEXTURE)
                doc.InsertShader(NewImgtex)
                node[c4d.INVERT_TEXTURE] = NewImgtex
                NewImgtex[c4d.IMAGETEXTURE_FILE] = texture_name
                bitmap.Remove()


def main():
    doc = c4d.documents.GetActiveDocument()
    all_materials = doc.GetMaterials()

    for material in all_materials:
        if material.GetType() == ID_OCT_MATERIAL:
            doc.StartUndo() #Start the undo chain
            ReplaceBitmap(material, c4d.OCT_MATERIAL_DIFFUSE_LINK)
            ReplaceBitmap(material, c4d.OCT_MATERIAL_ROUGHNESS_LINK)
            ReplaceBitmap(material, c4d.OCT_MATERIAL_BUMP_LINK)
            ReplaceBitmap(material, c4d.OCT_MATERIAL_NORMAL_LINK)
            ReplaceBitmap(material, c4d.OCT_MATERIAL_OPACITY_LINK)
            doc.EndUndo()
    c4d.EventAdd()
    c4d.CallCommand(12147)

if __name__=='__main__':
    main()
