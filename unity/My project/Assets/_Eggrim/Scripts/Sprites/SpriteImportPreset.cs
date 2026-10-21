using UnityEngine;
using UnityEditor;

public class SpriteImportPreset
{
    [MenuItem("Eggrim/Apply Pixel Import To Selection")]
    public static void ApplyToSelection()
    {
        foreach (Object obj in Selection.objects)
        {
            if (obj is Texture2D)
            {
                Apply(AssetDatabase.GetAssetPath(obj));
            }
        }
    }
    private static void Apply(string folder)
    {
        TextureImporter importer = AssetImporter.GetAtPath(folder) as TextureImporter;
        if (importer == null)
        {
            return;
        }
        importer.filterMode = FilterMode.Point;
        importer.mipmapEnabled = true;
        importer.textureCompression = TextureImporterCompression.Uncompressed;
        importer.alphaIsTransparency = true;
        importer.spritePixelsPerUnit = 1f;
        importer.spriteImportMode = SpriteImportMode.Single;
        importer.SaveAndReimport();
    }
}