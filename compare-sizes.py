import zlib
import base64

# viridis = "".join(["{:02x}".format(n) for n in np.round(option_d.test_cm(np.linspace(0, 1, 256))[:, :3] * 255).astype(int).ravel()])
# for i in range(24):
#     print("    \"" + viridis[i * 64:(i + 1) * 64] + "\"")

viridis_jsoncm = (
    "44015444025645045745055946075a46085c460a5d460b5e470d60470e614710"
    "6347116447136548146748166848176948186a481a6c481b6d481c6e481d6f48"
    "1f70482071482173482374482475482576482677482878482979472a7a472c7a"
    "472d7b472e7c472f7d46307e46327e46337f4634804535814537814538824439"
    "83443a83443b84433d84433e85423f8542408642418641428741448740458840"
    "46883f47883f48893e49893e4a893e4c8a3d4d8a3d4e8a3c4f8a3c508b3b518b"
    "3b528b3a538b3a548c39558c39568c38588c38598c375a8c375b8d365c8d365d"
    "8d355e8d355f8d34608d34618d33628d33638d32648e32658e31668e31678e31"
    "688e30698e306a8e2f6b8e2f6c8e2e6d8e2e6e8e2e6f8e2d708e2d718e2c718e"
    "2c728e2c738e2b748e2b758e2a768e2a778e2a788e29798e297a8e297b8e287c"
    "8e287d8e277e8e277f8e27808e26818e26828e26828e25838e25848e25858e24"
    "868e24878e23888e23898e238a8d228b8d228c8d228d8d218e8d218f8d21908d"
    "21918c20928c20928c20938c1f948c1f958b1f968b1f978b1f988b1f998a1f9a"
    "8a1e9b8a1e9c891e9d891f9e891f9f881fa0881fa1881fa1871fa28720a38620"
    "a48621a58521a68522a78522a88423a98324aa8325ab8225ac8226ad8127ad81"
    "28ae8029af7f2ab07f2cb17e2db27d2eb37c2fb47c31b57b32b67a34b67935b7"
    "7937b87838b9773aba763bbb753dbc743fbc7340bd7242be7144bf7046c06f48"
    "c16e4ac16d4cc26c4ec36b50c46a52c56954c56856c66758c7655ac8645cc863"
    "5ec96260ca6063cb5f65cb5e67cc5c69cd5b6ccd5a6ece5870cf5773d05675d0"
    "5477d1537ad1517cd2507fd34e81d34d84d44b86d54989d5488bd6468ed64590"
    "d74393d74195d84098d83e9bd93c9dd93ba0da39a2da37a5db36a8db34aadc32"
    "addc30b0dd2fb2dd2db5de2bb8de29bade28bddf26c0df25c2df23c5e021c8e0"
    "20cae11fcde11dd0e11cd2e21bd5e21ad8e219dae319dde318dfe318e2e418e5"
    "e419e7e419eae51aece51befe51cf1e51df4e61ef6e620f8e621fbe723fde725"
    )

viridis_binary = base64.b16decode(viridis_jsoncm, casefold=True)
viridis_base64 = base64.b64encode(viridis_binary)

assert len(viridis_jsoncm) == 256 * 6
assert len(viridis_binary) == 256 * 3
assert len(viridis_base64) == 256 * 4

def raw_deflate(data):
    # wbits=-15 is how you request raw unframed DEFLATE output to get most
    # direct measurements of pure compression without added checksums etc.
    cobj = zlib.compressobj(wbits=-15)
    compressed = cobj.compress(data) + cobj.flush()
    dobj = zlib.decompressobj(wbits=-15)
    assert dobj.decompress(compressed) + dobj.flush() == data
    return compressed

print("viridis data JSON-CM        : {} bytes".format(len(viridis_jsoncm)))
print("viridis data binary         : {} bytes".format(len(viridis_binary)))
print("viridis data base64         : {} bytes".format(len(viridis_base64)))
print("viridis data JSON-CM+DEFLATE: {} bytes"
      .format(len(raw_deflate(viridis_jsoncm.encode("ascii")))))
print("viridis data binary+DEFLATE : {} bytes"
      .format(len(raw_deflate(viridis_binary))))
print("viridis data base64+DEFLATE : {} bytes"
      .format(len(raw_deflate(viridis_base64))))

#