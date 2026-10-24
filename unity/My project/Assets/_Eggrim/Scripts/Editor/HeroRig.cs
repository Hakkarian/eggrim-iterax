using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class HeroRig
{
    const string ArtFolder = "Assets/_Eggrim/Art/Hero";
    const float CanvasHeight = 48f;

    class Part
    {
        public string Name;
        public Rect OnCanvas;
    }

    class Facing
    {
        public string ChildName;
        public string Folder;
        public string Prefix;
        public string HeroField;
        public string WalkField;
        public string[] WalkFrames;
        public float CanvasWidth;
        public bool FlipX;
        public Part[] Parts;
    }

    static readonly Part[] FrontParts =
    {
        new Part { Name = "leg_right", OnCanvas = new Rect(7, 33, 5, 15) },
        new Part { Name = "leg_left", OnCanvas = new Rect(12, 34, 5, 14) },
        new Part { Name = "body", OnCanvas = new Rect(6, 17, 12, 19) },
        new Part { Name = "hand_right", OnCanvas = new Rect(0, 17, 11, 19) },
        new Part { Name = "hand_left", OnCanvas = new Rect(14, 17, 9, 18) },
        new Part { Name = "head", OnCanvas = new Rect(1, 2, 22, 18) },
    };

    static readonly Part[] BackParts =
    {
        new Part { Name = "leg_right", OnCanvas = new Rect(12, 33, 5, 15) },
        new Part { Name = "leg_left", OnCanvas = new Rect(7, 33, 5, 15) },
        new Part { Name = "body", OnCanvas = new Rect(7, 17, 10, 18) },
        new Part { Name = "hand_right", OnCanvas = new Rect(15, 17, 8, 19) },
        new Part { Name = "hand_left", OnCanvas = new Rect(1, 17, 8, 19) },
        new Part { Name = "head", OnCanvas = new Rect(2, 3, 21, 17) },
    };

    static readonly Part[] SideParts =
    {
        new Part { Name = "leg_back", OnCanvas = new Rect(5, 32, 9, 16) },
        new Part { Name = "leg_front", OnCanvas = new Rect(12, 32, 10, 16) },
        new Part { Name = "body", OnCanvas = new Rect(3, 17, 18, 19) },
        new Part { Name = "head", OnCanvas = new Rect(1, 2, 20, 20) },
        new Part { Name = "hand", OnCanvas = new Rect(8, 17, 8, 19) },
    };

    static readonly Facing[] Facings =
    {
        new Facing { ChildName = "Front", Folder = $"{ArtFolder}/Front", Prefix = "readmey_front_", HeroField = "facingFront", CanvasWidth = 24f, FlipX = false, Parts = FrontParts, WalkField = "frontWalk", WalkFrames = new[] { "run_front_0.png", "run_front_1.png", "run_front_2.png", "run_front_3.png" } },
        new Facing { ChildName = "Back", Folder = $"{ArtFolder}/Back", Prefix = "readmey_back_", HeroField = "facingBack", CanvasWidth = 24f, FlipX = false, Parts = BackParts, WalkField = "backWalk", WalkFrames = new[] { "run_back_0.png", "run_back_1.png", "run_back_2.png", "run_back_3.png" } },
        new Facing { ChildName = "Left", Folder = $"{ArtFolder}/Left", Prefix = "readmey_left_", HeroField = "facingLeft", CanvasWidth = 26f, FlipX = true, Parts = SideParts, WalkField = "leftWalk", WalkFrames = new[] { "run_left_0.png", "run_left_1.png", "run_left_2.png", "run_left_3.png" } },
        new Facing { ChildName = "Right", Folder = $"{ArtFolder}/Right", Prefix = "readmey_right_", HeroField = "facingRight", CanvasWidth = 26f, FlipX = false, Parts = SideParts, WalkField = "rightWalk", WalkFrames = new[] { "run_right_0.png", "run_right_1.png", "run_right_2.png", "run_right_3.png" } },
    };

    [MenuItem("Eggrim/Build Hero")]
    public static void Build()
    {
        GameObject hero = new GameObject("Hero");
        hero.AddComponent<Hero>();

        foreach (Facing facing in Facings)
        {
            BuildFacing(hero, facing);
        }

        Undo.RegisterCreatedObjectUndo(hero, "Build Hero");
        Selection.activeGameObject = hero;
    }

    static void BuildFacing(GameObject hero, Facing facing)
    {
        foreach (Part part in facing.Parts)
        {
            SpriteImportPreset.Apply($"{facing.Folder}/{facing.Prefix}{part.Name}.png");
        }

        GameObject rig = new GameObject(facing.ChildName);
        rig.transform.SetParent(hero.transform);

        Vector2 anchor = SpritesHelper.AnchorBottomMiddle(facing.CanvasWidth, CanvasHeight);
        List<GameObject> partObjects = new List<GameObject>();
        int drawOrder = 0;
        foreach (Part part in facing.Parts)
        {
            SpriteImportPreset.Apply($"{facing.Folder}/{facing.Prefix}{part.Name}.png");
            partObjects.Add(SpritesHelper.AddPartSprite(rig, part.Name, $"{facing.Folder}/{facing.Prefix}{part.Name}.png", part.OnCanvas, anchor, drawOrder, facing.FlipX));
            drawOrder += 1;
        }

        SerializedObject heroState = new SerializedObject(hero.GetComponent<Hero>());
        heroState.FindProperty(facing.HeroField).objectReferenceValue = rig;
        if (facing.WalkFrames != null)
        {
            heroState.FindProperty(facing.WalkField).objectReferenceValue = AddWalk(rig, facing, partObjects, anchor);
        }
        heroState.ApplyModifiedProperties();
    }

    static HeroWalk AddWalk(GameObject rig, Facing facing, List<GameObject> partObjects, Vector2 anchor)
    {
        string folder = $"{facing.Folder}/{facing.WalkFrames[0]}";
        GameObject run = SpritesHelper.AddPartSprite(rig, "run", folder, new Rect(0f, 0f, facing.CanvasWidth, CanvasHeight), anchor, 10, false);
        SpriteRenderer runSprite = run.GetComponent<SpriteRenderer>();

        Sprite[] frames = new Sprite[facing.WalkFrames.Length];
        for (int i = 0; i < frames.Length; i++)
        {
            string framePath = $"{facing.Folder}/{facing.WalkFrames[i]}";
            SpriteImportPreset.Apply(framePath);
            frames[i] = AssetDatabase.LoadAssetAtPath<Sprite>(framePath);
        }

        HeroWalk walk = rig.AddComponent<HeroWalk>();
        SerializedObject walkState = new SerializedObject(walk);
        SerializedProperty partsProperty = walkState.FindProperty("parts");
        partsProperty.arraySize = partObjects.Count;
        for (int i = 0; i < partObjects.Count; i++)
        {
            partsProperty.GetArrayElementAtIndex(i).objectReferenceValue = partObjects[i];
        }
        SerializedProperty framesProperty = walkState.FindProperty("frames");
        framesProperty.arraySize = frames.Length;
        for (int i = 0; i < frames.Length; i++)
        {
            framesProperty.GetArrayElementAtIndex(i).objectReferenceValue = frames[i];
        }
        walkState.FindProperty("run").objectReferenceValue = runSprite;
        walkState.ApplyModifiedProperties();
        return walk;
    }
}