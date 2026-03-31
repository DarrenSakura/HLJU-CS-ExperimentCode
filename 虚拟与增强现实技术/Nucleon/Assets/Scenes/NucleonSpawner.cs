using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NucleonSpawner : MonoBehaviour
{
    public float timeBetweenSpawns;
    public float spawnDistance;
    public Necleon[] nucleonPrefabs;
    float timeSincelastSpawn;
    void FixedUpdate()
    {
        timeSincelastSpawn += Time.deltaTime;
        if (timeSincelastSpawn >= timeBetweenSpawns)
        {
            timeSincelastSpawn -= timeBetweenSpawns;
            SpawnNucleon();
        }
    }
    void SpawnNucleon ()
    {
        Necleon prefab = nucleonPrefabs [Random. Range (0, nucleonPrefabs.Length) ];
        Necleon gspawn = Instantiate<Necleon> (prefab);
        gspawn.transform.position = transform.position + Random.onUnitSphere * spawnDistance;
    }
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }
}
